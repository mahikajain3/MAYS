"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus
from flask import Flask
# from flask_cors import CORS
from flask_restx import Resource, Api, reqparse
import werkzeug.exceptions as wz
import db.data as db

app = Flask(__name__)
# CORS(app)
api = Api(app)

ns_user = api.namespace('users', description='user related endpoints')
ns_badge = api.namespace('badges', description='badge related endpoints')
ns_training = api.namespace('trainings',
                            description='training related endpoints')
ns_workshop = api.namespace('workshops',
                            description='workshop related endpoints')


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


@api.route('/login/<username>/<password>')
class Login(Resource):
    """
    This endpoint is for the login.
    """

    @api.response(HTTPStatus.OK, 'Success')
    def post(self, username, password):
        """
        Login to the site.
        """
        if db.netid_exists(username):
            if password != db.get_password(username):
                raise (wz.NotFound("Wrong password.\
                    Please try again."))
            else:
                return "success."
        else:
            raise (wz.NotFound("Wrong username.\
                Please try again."))

        """ if (username != 'admin' or
                password != 'admin'):
            raise (wz.NotFound("Wrong username or password.\
                Please try again."))
        else:
            return "success." """


@ns_user.route('/list')
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


user_parser = reqparse.RequestParser()
user_parser.add_argument('firstname')
user_parser.add_argument('lastname')
user_parser.add_argument('barcode')


@ns_user.route('/create/<netid>')
class CreateUser(Resource):
    """
    This endpoint adds a new user to the list of all the users.
    """
    @api.doc(parser=user_parser)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, netid):
        """
        This method adds a new user to the list of all users.
        """
        args = user_parser.parse_args()
        firstname = args['firstname']
        lastname = args['lastname']
        barcode = args['barcode']
        ret = db.add_user(netid, firstname, lastname, barcode)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("List of users db not found."))
        elif ret == db.DUPLICATE:
            raise (wz.NotAcceptable("User name already exists."))
        else:
            return f"{netid} added."


@ns_user.route('/update/<oldnetid>/<newnetid>')
class UpdateUser(Resource):
    """
    This endpoint allows the user to update a user name.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def put(self, oldnetid, newnetid):
        """
        This method updates old user name to new user name.
        """
        ret = db.update_user(oldnetid, newnetid)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("User not found."))
        elif ret == db.DUPLICATE:
            raise (wz.NotAcceptable("User name already exists."))
        else:
            return f"{oldnetid} updated to {newnetid}."


@ns_user.route('/delete/<username>')
class DeleteUser(Resource):
    """
    This endpoint removes an existed user from the list of all the users.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def delete(self, username):
        """
        This method removes an existed user from the list of all users.
        """
        ret = db.del_user(username)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("This user does not exist in the users list."))
        else:
            return f"{username} deleted."


badge_parser = reqparse.RequestParser()
badge_parser.add_argument('description')
badge_parser.add_argument('trainingname', action='split')
badge_parser.add_argument('workshopname', action='split')


@ns_badge.route('/create/<badgename>')
class CreateBadges(Resource):
    """
    This endpoint adds:
    a new badge to the list of all the badges,
    workshops to the list of all the workshops
    (if it doesn't already exist),
    trainings to the list of all the trainings
    (if it doesn't already exist)
    """
    @api.doc(parser=badge_parser)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, badgename):
        """
        This method adds a new badge to the list of all badges.
        It has the option to add trainings, workshops as well.
        Need to add descriptions. !!!!!
        """
        args = badge_parser.parse_args()
        desc = args["description"]
        traininglist = args["trainingname"]
        workshoplist = args["workshopname"]
        ret = db.add_badge(badgename, desc)

        if workshoplist:
            for wkshp in workshoplist:
                if not (db.workshop_exists(wkshp)):
                    db.add_workshop(wkshp)
        if traininglist:
            for train in traininglist:
                if not (db.training_exists(train)):
                    db.add_training(train)

        if ret == db.NOT_FOUND:
            raise (wz.NotFound("List of badges db not found."))
        elif ret == db.DUPLICATE:
            raise (wz.NotAcceptable("Badge name already exists."))
        else:
            return f"{badgename} added."


@ns_badge.route('/list')
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


@ns_badge.route('/list/<badgename>')
class GetBadgesByID(Resource):
    """
    This endpoint return info of a specific badge.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, badgename):
        """
        This endpoint return info of a specific badge.
        """
        badges = db.get_badge_by_id(badgename)
        if badges is None:
            raise (wz.NotFound("Badge does not exist."))
        else:
            return badges


# badge_parser = reqparse.RequestParser()
# badge_parser.add_argument('new_badgename', type=str, help='new_badgename')
# badge_parser.add_argument('new_trainingname',
# type=str, help='new_trainingname')
# badge_parser.add_argument('new_workshopname',
# type=str, help='new_workshopname')


@ns_badge.route('/update/<oldbadgename>/<newbadgename>/<newdescription>')
class UpdateBadges(Resource):
    """
    This endpoint allows the user to update a badge name.
    """

    # @api.doc(parser=badge_parser)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def put(self, old_badgename, new_badgename, desc):
        """
        This method updates old badge name to new
        badge name and new description.
        """
        # args = badge_parser.parse_args()
        # new_badgename = args['new_badgename']
        ret = db.update_badge(old_badgename, new_badgename)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("Badge not found."))
        elif ret == db.DUPLICATE:
            raise (wz.NotAcceptable("Badge name already exists."))
        elif len(desc) != 0:
            db.update_badge_desc(new_badgename, desc)
        else:
            return f"{old_badgename} updated to {new_badgename}."


@ns_badge.route('/delete/<badgename>')
class DeleteBadge(Resource):
    """
    This endpoint removes an existed badge.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def delete(self, badgename):
        """
        This method removes an existed badge from the list of all badges.
        """
        ret = db.del_badge(badgename)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("Badge does not exist."))
        else:
            return f"{badgename} deleted."


@ns_training.route('/create/<trainingname>')
class CreateTrainings(Resource):
    """
    This endpoint adds a new training to the list of all the trainings.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def post(self, trainingname):
        """
        This method adds a new training to the list of all trainings.
        """
        ret = db.add_training(trainingname)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("List of trainings db not found."))
        elif ret == db.DUPLICATE:
            raise (wz.NotAcceptable("Training name already exists."))
        else:
            return f"{trainingname} added."


@ns_training.route('/list')
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


@ns_training.route('/update/<oldtrainingname>/<newtrainingname>')
class UpdateTrainings(Resource):
    """
    This endpoint allows the user to update a training name.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def put(self, oldtrainingname, newtrainingname):
        """
        This method updates old training name to new training name.
        """
        ret = db.update_training(oldtrainingname, newtrainingname)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("Training not found."))
        elif ret == db.DUPLICATE:
            raise (wz.NotAcceptable("Training name already exists."))
        else:
            return f"{oldtrainingname} updated to {newtrainingname}."


@ns_training.route('/delete/<trainingname>')
class DeleteTraining(Resource):
    """
    This endpoint removes an existed training from the trainings.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def delete(self, trainingname):
        """
        This method removes an existed training from the list of all trainings.
        """
        ret = db.del_training(trainingname)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("Training does not exist."))
        else:
            return f"{trainingname} deleted."


@ns_workshop.route('/create/<workshopname>')
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


@ns_workshop.route('/list')
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


@ns_workshop.route('/update/<oldwsname>/<newwsname>')
class UpdateWorkshops(Resource):
    """
    This endpoint allows the user to update a badge name.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def put(self, oldwsname, newwsname):
        """
        This method updates old workshop name to new workshop name.
        """
        ret = db.update_workshop(oldwsname, newwsname)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("Workshop not found."))
        elif ret == db.DUPLICATE:
            raise (wz.NotAcceptable("Workshop name already exists."))
        else:
            return f"{oldwsname} updated to {newwsname}."


@ns_workshop.route('/delete/<workshopname>')
class DeleteWorkshop(Resource):
    """
    This endpoint removes an existed workshop from the workshops.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key')
    def delete(self, workshopname):
        """
        This method removes an existed workshop from the list of all workshops.
        """
        ret = db.del_workshop(workshopname)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("Workshop does not exist."))
        else:
            return f"{workshopname} deleted."
