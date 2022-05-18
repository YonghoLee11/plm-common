import datetime
import json
from flask import request, current_app
import os
from log import logger
from rediscluster import RedisCluster
import json
import re
import time

def getSetSessionObj():
    '''
        request헤더의 meta.uuid를 사용하여 레디스에 세션정보 로드
    '''
   
    sessionObj = {
        'USER_ID': '',
        'EMP_NO': '',
        'NAME_KOR': '',
        'NAME_ENG': '',
        'NAME_CHN': '',
        'DEPT_ID': '',
        'DEPT_NAME_KOR': '',
        'DEPT_NAME_ENG': '',
        'DEPT_NAME_CHN': '',
        'uuid' : '',
        'client' : ''
    }

    try:
        if ('HTTP_META' in request.environ.keys()):
            meta = json.loads(request.environ['HTTP_META'])
            
            redis_info = get_sessionredis_info()
            rc = RedisCluster(startup_nodes=redis_info['info'], password=redis_info['password'], decode_responses=True)
            rSessionUuid = 'SN:{}'.format(meta['uuid'])
            sessionInfo = rc.get(rSessionUuid)
            sessionObj = json.loads(sessionInfo)
            return sessionObj
                
    except Exception as e:
        logger.error("sessionObj Error: {}".format(e))

    return sessionObj

def browserWithVersion(userAgentString):
    '''
        http 헤더의 useragent를 분석하여 웹 브라우저 정보 파싱
        1. flask에서 자동 파싱한 값을 리턴
        2. userAgentString가 없는 경우에는 unknown리턴
    '''
    # default value
    browser_name = 'Unknown'
    browser_version = 'Unknown'

    if userAgentString:
        browser_name = userAgentString.browser
        browser_version = userAgentString.version

    return "{} {}".format(browser_name, browser_version)

def initAccessLog():

    logObj = {
        'clientIp': '',
        'IPS': '',
        'rscId' : '',
        'sessionId': '',
        'client': '',
        'api': '',
        'userId': '',
        'userName': '',
        'userDeptName': '',
        'referer': '',
        'isError': 0,
        'errorStack': '',
        'timestamp': '',
        'tarceId': '',
        'trxId': '',
        'system_id': '',
        'browser': '',
        'locId': '',
        'app': '',
        'target': ''
    }

    try:
        ip = request.headers.get('X-Real-IP')
        host = request.headers.get('host')
        KST = datetime.timezone(datetime.timedelta(hours=9))
        now = datetime.datetime.now(tz=KST).strftime("%Y-%m-%dT%H:%M:%S.%f+0900")
        now_int = int(time.time())
        request_url = request.path
        hcpConfiguration = get_hcpconfiguration()
        if hcpConfiguration is None:
            hcpConfiguration = {}

        if ip is None and host:
            ip = host.split("\\:")[0]
        if ip and "," in ip:
            logObj['IPS'] = ip
            ip = ip.split("\\,")[0].strip()

        empNo = request.sessionObj.get('EMP_NO')
        if empNo is None:
            empNo = request.cookies.get('LASTUSER')
            if empNo is None:
                empNo = ip

        logObj['clientIp'] = ip
        logObj['rscId'] = hcpConfiguration.get('SVC_ID')
        logObj['sessionId'] = request.sessionObj.get('uuid')
        logObj['client'] = request.sessionObj.get('client')
        logObj['api'] = request_url
        logObj['userId'] = empNo
        logObj['userName'] = request.sessionObj.get('NAME_KOR')
        logObj['userDeptName'] = request.sessionObj.get('DEPT_NAME_KOR')
        logObj['referer'] = request.referrer if request.referrer else "Unknown"
        logObj['timestamp'] = now

        if request.args.get('tarceId'):
            logObj['tarceId'] = request.args.get('tarceId')
        else:
            logObj['tarceId'] = "{}:{}:{}".format(request_url, now_int, ip)
        if request.args.get('trxId'):
            logObj['trxId'] = request.args.get('trxId')
        else:
            logObj['trxId'] = "{}:{}".format(request_url, now_int)
        # 검토필요
        if request.args.get('system_id'):
            logObj['system_id'] = request.args.get('system_id')
        else:
            logObj['system_id'] = host
        logObj['browser'] = browserWithVersion(request.user_agent)
        logObj['locId'] = hcpConfiguration.get('LOCID')
        logObj['app'] = hcpConfiguration.get('APP')
        logObj['target'] = hcpConfiguration.get('TARGET')
    except Exception as e:
        logger.error("initAccessLog error: {}".format(e))

    return logObj

def executeAccessLog(response):
    '''
        1. 로그 출력
        2. redis에 로그 저장
    '''
    try:
        if request.access_log:
            responseTime = float(get_APIExecutionTime() * 1000)
            logObj = request.access_log
            response_code = int(response.status_code)
            hcpConfiguration = get_hcpconfiguration()
            if hcpConfiguration is None:
                hcpConfiguration = {}

            # http status_code가 200이 아니면서 오류코드(ex: 404)인 경우
            if response_code != 200 and hasattr(response, 'http_error'):
                logObj['isError'] = 1
                logObj['errorStack'] = "{}:{}:{}".format(
                    response.http_error.get('code'),
                    response.http_error.get('msg'),
                    response.http_error.get('desc')
                )

            hostname = os.getenv('hostname')
            logObj['taskId'] = hostname if hostname else ''
            logObj['service_id'] = hcpConfiguration.get('SVC_ID')
            logObj['env'] = hcpConfiguration.get('ENV')
            logObj['prjId'] = hcpConfiguration.get('PRJ_ID')
            logObj['responseTime'] = responseTime
            logObj['service_full_id'] = "/hcp/{}/{}/{}".format(
                hcpConfiguration.get('PRJ_ID'), 
                hcpConfiguration.get('ENV'),
                hcpConfiguration.get('SVC_ID'),
                )
            logObj['responseCode'] = response_code

            # 로그를 큐에 push
            log_queue = hcpConfiguration['REDIS_LOG_QUEUE']
            desired_log_size = hcpConfiguration['REDIS_LOG_SIZE']
            
            log_queue.append(logObj)

            # 로그 stdout 출력
            logger.info("accessLog => {}".format(logObj))

            # 큐에 쌓여있는 로그가 1000(desired_log_size)개 이상일 경우 redis에 로그 전송
            if len(log_queue) > desired_log_size:
                log_to_redis()
            
        else:
            logger.error("[Error] executeAccessLog -> request.access_log is not exist")
    except Exception as e:
        logger.error("[Error] executeAccessLog error {}".format(e))

def log_to_redis():
    '''
        최대 로그 1000(config.py REDIS_LOG_SIZE)개를 redis에 전송
    '''
    hcpConfiguration = get_hcpconfiguration()
    log_queue = hcpConfiguration['REDIS_LOG_QUEUE']
    desired_log_size = hcpConfiguration['REDIS_LOG_SIZE']

    queue_size = len(log_queue)
    queue_size = desired_log_size if queue_size > desired_log_size else queue_size

    logs = [log_queue.popleft() for _ in range(0, queue_size)]
    if len(logs) > 0:
        redis_info = get_sessionredis_info()
        rc = RedisCluster(startup_nodes=redis_info['info'], password=redis_info['password'], decode_responses=True)
        rc.lpush(hcpConfiguration['REDIS_LOG_KEY'], json.dumps(logs))

def get_APIExecutionTime():
    """
        API실행시간 계산
    """
    return  request.end_time - request.start_time

def exclude_logpattern():
    '''
        로그 제외 url패턴
        리턴: 
            True: 로깅 제외
            False: 로깅 제외하지 않음
    '''
    hcpconfiguration = get_hcpconfiguration()

    # test_patterns = ["/swagger(.*)[/]?.+"]

    # 정확한 일치 검사패턴
    exactly_patterns = [
        "/", 
        "/favicon.ico", 
    ]

    # 정규식 검사패턴
    regex_patterns = 'swagger-ui|swaggerui|swagger.json$'

    for pattern in exactly_patterns:
        if request.path == pattern:
            return True
    
    p = re.compile(regex_patterns)
    if p.search(request.path):
        return True

    return False

def get_redisinfo():
    '''
        리턴: 로그 레디스 접속정보(host, port)
    '''
    return [{
        'host': current_app.__dict__.get('config')['REDIS_HOST'],
        'port': current_app.__dict__.get('config')['REDIS_PORT']
    }]  

def get_sessionredis_info():
    '''
        리턴: 세션 레디스 접속정보(host, port, password)
    '''
    return {
        "info": [{
            'host': current_app.__dict__.get('config')['SESSION_REDIS_HOST'],
            'port': current_app.__dict__.get('config')['SESSION_REDIS_PORT']
        }],
        "password": current_app.__dict__.get('config')['SESSION_REDIS_PASSWORD']
    }    

def get_hcpconfiguration():
    '''
        flask app config(config.py)리턴
    '''
    return current_app.__dict__.get('config')

def accessLogs(response):
    if not exclude_logpattern():
        request.sessionObj = getSetSessionObj()
        request.access_log = initAccessLog()
        executeAccessLog(response)
