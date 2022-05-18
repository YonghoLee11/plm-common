from flask_restplus import fields
from api import api, db, logger

logger.debug("=====models todo=====")

# API 명세를 작성한다.
todo = api.model('Todo', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})

# Model class 를 작성한다.
class Todo(db.Model):
    logger.debug('=====Model Todo=====')

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(128))

    def __init__(self, task):
        self.task = task
