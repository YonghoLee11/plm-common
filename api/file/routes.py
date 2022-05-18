from flask import Flask
from flask_restplus import Resource
from api import api, logger
from .dao import dao
from .models import file

logger.debug("=====routes file=====")

# 기본경로를 app/todos 로 설정해준다.
ns = api.namespace('files', description='FILE operations description')

# /todos/ route
@ns.route('/')
class Todos(Resource):
    # Shows a list of all todos, and lets you POST to add new tasks
    @ns.doc('list_files', description='list_files description')
    @ns.marshal_list_with(file)
    def get(self):
        logger.debug("=====get file list=====")

        # List all file
        return dao.get_list()

    @ns.doc('create_todo', description='create_todo description')
    @ns.expect(file)
    @ns.marshal_with(file, code=201)
    def post(self):
        logger.debug("=====create file=====")
        logger.debug(api.payload)

        # Create a new file
        return dao.create(api.payload), 201

# /todos/<int:id> route
@ns.route('/<int:id>')
@ns.response(404, 'file not found')
@ns.param('id', 'The file identifier')
class File(Resource):
    # Show a single file file and lets you delete them
    @ns.doc('get_todo', description='get_todo description')
    @ns.marshal_with(file)
    def get(self, id):
        logger.debug("=====get file=====")
    
        # Fetch a given resource
        return dao.get(id)

    @ns.doc('delete_todo', description='delete_todo description')
    @ns.response(204, 'file deleted')
    def delete(self, id):
        logger.debug("=====delete file=====")

        # Delete a file given its identifier
        dao.delete(id)
        return '', 204

    @ns.doc('update_todo', description='update_todo description')
    @ns.expect(file)
    @ns.marshal_with(file)
    def put(self, id):
        logger.debug("=====update file=====")

        # Update a file given its identifier
        return dao.update(id, api.payload)
