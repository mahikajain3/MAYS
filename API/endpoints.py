"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus
from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api
import werkzeug.exceptions as wz
import db.data as db

app = Flask(__name__)
CORS(app)
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


@api.route('/badges/create/<badgename>')
class CreateBadges(Resource):
    """
    This endpoint adds a new training to the list of all the trainings.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, badgename):
        """
        This method adds a new user to the list of all users.
        """
        ret = db.add_badge(badgename)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("List of trainings db not found."))
        elif ret == db.DUPLICATE:
            raise (wz.NotAcceptable("Training name already exists."))
        else:
            return f"{badgename} added."


@api.route('/badges/list')
class ListBadges(Resource):
    """
    This endpoint return a list of all the badges.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self):
        """
        Returns list of all badges.
        """
        badges = db.get_badges()
        if badges is None:
            raise (wz.NotFound("List of badges db not found."))
        else:
            return badges


@api.route('/trainings/create/<trainingname>')
class CreateTrainings(Resource):
    """
    This endpoint adds a new training to the list of all the trainings.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, trainingname):
        """
        This method adds a new user to the list of all users.
        """
        ret = db.add_training(trainingname)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("List of trainings db not found."))
        elif ret == db.DUPLICATE:
            raise (wz.NotAcceptable("Training name already exists."))
        else:
            return f"{trainingname} added."


@api.route('/trainings/list')
class ListTrainings(Resource):
    """
    This endpoint return a list of all the trainings.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self):
        """
        Returns list of all trainings.
        """
        trainings = db.get_trainings()
        if trainings is None:
            raise (wz.NotFound("List of trainings db not found."))
        else:
            return trainings


@api.route('/workshops/create/<workshopname>')
class CreateWorkshops(Resource):
    """
    This endpoint adds a new workshop to the list of all the workshops.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, workshopname):
        """
        This method adds a new user to the list of all users.
        """
        ret = db.add_workshop(workshopname)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("List of workshops db not found."))
        elif ret == db.DUPLICATE:
            raise (wz.NotAcceptable("Workshop name already exists."))
        else:
            return f"{workshopname} added."


@api.route('/workshops/list')
class ListWorkshops(Resource):
    """
    This endpoint return a list of all the workshops.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self):
        """
        Returns list of all workshops.
        """
        workshops = db.get_workshops()
        if workshops is None:
            raise (wz.NotFound("List of workshops db not found."))
        else:
            return workshops


@api.route('/workshops/delete/<workshopname>')
class DeleteWorkshop(Resource):
    """
    This endpoint removes an existed workshop from the workshops.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, workshopname):
        """
        This method removes an existed user from the list of all users.
        """
        ret = db.del_workshop(workshopname)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("Workshop does not exist in the workshop list."))
        else:
            return f"{workshopname} deleted."


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


@api.route('/users/delete/<username>')
class DeleteUser(Resource):
    """
    This endpoint removes an existed user from the list of all the users.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, username):
        """
        This method removes an existed user from the list of all users.
        """
        ret = db.del_user(username)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("This user does not exist in the users list."))
        else:
            return f"{username} deleted."


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
