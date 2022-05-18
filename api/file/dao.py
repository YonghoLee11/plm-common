from api import api, db, logger
from .models import File

class FileDAO(object):
    def __init__(self):
        logger.debug("=====__init__=====")

    def get_list(self):
        logger.debug("=====get_list=====")

        return File.query.all()

    def get(self, id):
        logger.debug("=====get=====")

        return File.query.get(id)

    def create(self, data):
        logger.debug("=====create=====")
        logger.debug(data)

        file = File(data['filename'])

        try:
            db.session.add(file)
            db.session.commit()
        except Exception as ex:
            logger.error('add error', ex)
            api.abort(500, "add error")

        return file

    def update(self, id, data):
        logger.debug("=====update=====")

        file = File.query.get(id)
        file.file = data['filename']

        try:
            db.session.commit()
        except Exception as ex:
            logger.error('update error', ex)
            api.abort(500, "update error")

        return file

    def delete(self, id):
        logger.debug("=====delete=====")
        
        file = File.query.get(id)

        try:
            db.session.delete(file)
            db.session.commit()
        except Exception as ex:
            logger.error('delete error', ex)
            api.abort(500, "delete error")

logger.debug("=====dao file=====")

dao = FileDAO()

# Sample Data 입력
# dao.create({'filename': 'Build an API'})
# dao.create({'filename': '한글 입력 테스트'})
# dao.create({'filename': 'profit!'})