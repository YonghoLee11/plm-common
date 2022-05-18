import logging
import logging.config
import yaml
import os

# os.makedirs("/var/log/app", exist_ok=True)

# log.yml 파일을 읽어서 yaml 로딩
with open('log.yaml', 'r', encoding='UTF8') as f:
  log_cfg = yaml.safe_load(f.read())
 
# dictConfig 로 할당
logging.config.dictConfig(log_cfg)
 
# logger 가져오기
logger = logging.getLogger('simpleLogger')
 
# 각 로그 테스트
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')