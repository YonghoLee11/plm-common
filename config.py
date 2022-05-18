from collections import deque

# config.py
apiVersion = '1.0.0'
with open(".version", "r", encoding='UTF8') as fh:
    apiVersion = fh.read()

class Config:
    # 변경시 아래 포맷을 유지해주세요.
    PRJ_ID = 'plm'
    PRJ_ALIAS = 'plm'
    SVC_TYPE = 'python'
    SVC_ID = 'plm-python-common'
    
    LOCID = 'hy-koic-k8s-app-d01'
    TARGET = 'basic'
    APP = 'plm-python-common-basic-dev'

    APP_NAME = 'plm-python-common'
    API_VERSION = apiVersion
    API_TITLE = 'HCP Microservice plm-python-common'
    API_DESC = 'A plm-python-common API description'
    
    # API Path 를 변경할 경우 deployment.yml, ingress.yml 를 같이 변경해줘야 합니다. 
    API_PATH = '/plm-python-common' # do not modify
    API_DOC_PATH = '/swagger-ui/' # do not modify
    
    # 개발자 정보로 변경해주세요.
    APP_AUTHOR = 'X0000000'
    APP_AUTHOR_EMAIL = 'skhy.X0000000@partner.sk.com'

    # 레디스에 push하는 로그 키
    REDIS_LOG_KEY = 'TASK:LOG'

    # 레디스 큐
    REDIS_LOG_QUEUE = deque()

    # 로그 큐를 레디스에 push하는 크기
    REDIS_LOG_SIZE = 1000

    # 로그 스케쥴러 설정
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "Asia/Seoul"

    # 세션 레디스
    SESSION_REDIS_HOST = "10.158.123.69"
    SESSION_REDIS_PORT = "10003"
    SESSION_REDIS_PASSWORD = "redisadmin123!"
    
class LocalConfig(Config):
    DEBUG = True
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = "portaldev.skhynix.com"
    REDIS_PORT = "30285"
    ENV = "dev"

class DevConfig(Config):
    DEBUG = True
    TESTING = True
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = "portaldev.skhynix.com"
    REDIS_PORT = "30285"
    ENV = "dev"

class StgConfig(Config):
    DEBUG = True
    TESTING = True
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = "portaldev.skhynix.com"
    REDIS_PORT = "30285"
    ENV = "stg"

class PrdConfig(Config):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = "workplace.skhynix.com"
    REDIS_PORT = "10285"
    ENV = "prd"

config_by_name = dict(
	local=LocalConfig,
	dev=DevConfig,
    stg=StgConfig,
	prd=PrdConfig
)