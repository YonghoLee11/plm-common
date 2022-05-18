from app import application, logger

logger.debug("=====run.py=====")

# server start
if __name__ == "__main__":
    application.run(host = '127.0.0.1')