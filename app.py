import os
from flask import Flask, render_template, request
from werkzeug.exceptions import HTTPException
from log import logger
from config import Config, config_by_name
import accessLog
import time
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from accessLog import log_to_redis
import logging

application = Flask(__name__)

# config 를 넣어준다.
mode = os.getenv('spring.profiles.active') or 'local'
logger.debug("mode => " + mode)
application.config.from_object(config_by_name[mode])
application.secret_key = 'flasknotewithsqlalchemy'

# api import
import api

# 백그라운드 스케쥴러 등록
scheduler = APScheduler(scheduler=BackgroundScheduler(timezone="Asia/Seoul"))
scheduler.init_app(application)
scheduler.start()
logging.getLogger('apscheduler').setLevel(logging.WARNING)

# render_template
@application.route('/')
def index():
    return render_template('index.html', config=Config)

@application.before_request
def before_request():
    '''
        API실행 전 시간 확인
    '''
    request.start_time = time.time()

@application.after_request
def doLogger(response):
    # API 종료시간 확인
    request.end_time = time.time()

    # livenessProbe 용도
    if not os.getenv('rscId', default="") + '/application/info' in request.url:
        accessLog.accessLogs(response)

    return response

@application.errorhandler(HTTPException)
def error(e):
    """
        HTTP 에러 핸들링
    """
    response = e.get_response()

    errorObj = {
        'code': e.code,
        'msg' : e.name,
        'desc': e.description,
    }
    response.http_error = errorObj

    return response

@scheduler.task("interval", id="do_job_1", seconds=1, misfire_grace_time=900)
def job1():
    '''
        flask 스케쥴러
            큐에 저장되어 있는 로그를 1분마다 redis에 전송
    '''
    with application.app_context():
        log_to_redis()
