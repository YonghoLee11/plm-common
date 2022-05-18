from flask import Flask
from flask_restplus import Resource
from api import api, logger
from .dao import dao
from .models import todo

logger.debug("=====routes todo=====")

# 기본경로를 app/todos 로 설정해준다.
ns = api.namespace('todos', description='TODO operations description')

# /todos/ route
@ns.route('/')
class Todos(Resource):
    # Shows a list of all todos, and lets you POST to add new tasks
    @ns.doc('list_todos', description='list_todos description')
    @ns.marshal_list_with(todo)
    def get(self):
        logger.debug("=====get todo list=====")

        # List all todo
        return dao.get_list()

    @ns.doc('create_todo', description='create_todo description')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        logger.debug("=====create todo=====")
        logger.debug(api.payload)

        # Create a new todo
        return dao.create(api.payload), 201

# /todos/<int:id> route
@ns.route('/<int:id>')
@ns.response(404, 'todo not found')
@ns.param('id', 'The todo identifier')
class Todo(Resource):
    # Show a single todo todo and lets you delete them
    @ns.doc('get_todo', description='get_todo description')
    @ns.marshal_with(todo)
    def get(self, id):
        logger.debug("=====get todo=====")
    
        # Fetch a given resource
        return dao.get(id)

    @ns.doc('delete_todo', description='delete_todo description')
    @ns.response(204, 'todo deleted')
    def delete(self, id):
        logger.debug("=====delete todo=====")

        # Delete a todo given its identifier
        dao.delete(id)
        return '', 204

    @ns.doc('update_todo', description='update_todo description')
    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        logger.debug("=====update todo=====")

        # Update a todo given its identifier
        return dao.update(id, api.payload)
