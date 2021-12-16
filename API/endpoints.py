"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus
from flask import Flask
from flask_restx import Resource, Api
import werkzeug.exceptions as wz
import db.data as db


app = Flask(__name__)
api = Api(app)

HELLO = 'Hola'
WORLD = 'mundo'


@api.route('/hello')
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO: WORLD}


@api.route('/users/list')
class ListUsers(Resource):
    """
    This endpoint return a list of all the users.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self):
        """
        Returns list of all users.
        """
        users = db.get_users()
        if users is None:
            raise (wz.NotFound("List of users db not found."))
        else:
            return users


@api.route('/users/create/<username>')
class CreateUser(Resource):
    """
    This endpoint adds a new user to the list of all the users.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, username):
        """
        This method adds a new user to the list of all users.
        """
        ret = db.add_user(username)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("List of users db not found."))
        elif ret == db.DUPLICATE:
            raise (wz.NotAcceptable("User name already exists."))
        else:
            return f"{username} added."


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    @api.response(HTTPStatus.OK, 'Success')
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route('/pets/<username>')
class Pets(Resource):
    """
    This class supports fetching a list of all pets.
    """
    @api.response(HTTPStatus.OK, 'Success')
    def post(self, username):
        """
        This method returns all pets.
        """
        return username
