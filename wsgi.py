from app import application, logger

logger.debug("=====wsgi.py=====")

# server start
if __name__ == "__main__":
    application.run(host = '0.0.0.0')