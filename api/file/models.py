from flask_restplus import fields
from api import api, db, logger

logger.debug("=====models file=====")

# API 명세를 작성한다.
file = api.model('File', {
    'id': fields.Integer(readOnly=True, description='The file unique identifier'),
    'filename': fields.String(required=True, description='The filename details')
})

# Model class 를 작성한다.
class File(db.Model):
    logger.debug('=====Model File=====')

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128))

    def __init__(self, filename):
        self.filename = filename
