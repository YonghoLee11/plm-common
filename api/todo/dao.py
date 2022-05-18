from api import api, db, logger
from .models import Todo

class TodoDAO(object):
    def __init__(self):
        logger.debug("=====__init__=====")

    def get_list(self):
        logger.debug("=====get_list=====")

        return Todo.query.all()

    def get(self, id):
        logger.debug("=====get=====")

        return Todo.query.get(id)

    def create(self, data):
        logger.debug("=====create=====")
        logger.debug(data)

        todo = Todo(data['task'])

        try:
            db.session.add(todo)
            db.session.commit()
        except Exception as ex:
            logger.error('add error', ex)
            api.abort(500, "add error")

        return todo

    def update(self, id, data):
        logger.debug("=====update=====")

        todo = Todo.query.get(id)
        todo.task = data['task']

        try:
            db.session.commit()
        except Exception as ex:
            logger.error('update error', ex)
            api.abort(500, "update error")

        return todo

    def delete(self, id):
        logger.debug("=====delete=====")
        
        todo = Todo.query.get(id)

        try:
            db.session.delete(todo)
            db.session.commit()
        except Exception as ex:
            logger.error('delete error', ex)
            api.abort(500, "delete error")

logger.debug("=====dao todo=====")

dao = TodoDAO()

# Sample Data 입력
# dao.create({'task': 'Build an API'})
# dao.create({'task': '한글 입력 테스트'})
# dao.create({'task': 'profit!'})