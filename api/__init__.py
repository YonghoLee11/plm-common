from flask import Blueprint
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from log import logger
from config import Config
from app import application

logger.debug("=====api/__init__=====")

# API 명세
blueprint = Blueprint('api', __name__, url_prefix=Config.API_PATH) # , url_prefix = API_PATH
api = Api(blueprint, version=Config.API_VERSION, title=Config.API_TITLE, description=Config.API_DESC, doc=Config.API_DOC_PATH) # , doc = API_DOC_PATH
application.register_blueprint(blueprint)

# db 연결
db = SQLAlchemy(application)

# api
from . import todo, file