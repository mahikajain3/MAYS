"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import os
import json
from bson import json_util

import db.db_connect as dbc

MAYS_HOME = os.environ["MAYS_HOME"]

# collection name
USERS = "users"
TRAININGS = "trainings"
BADGES = "badges"
WORKSHOPS = "workshops"

# field names in our DB:
USERS_NM = "userName"
# PASSWORD = " password"
NETID = "netid"
FIRST_NM = "firstName"
LAST_NM = "lastName"
BARCODE = "barcode"

TRAININGS_NM = "trainingName"
BADGES_NM = "badgeName"
DESC = "description"
WORKSHOPS_NM = "workshopName"

OK = 0
NOT_FOUND = 1
DUPLICATE = 2

# DEMO_HOME = os.environ["DEMO_HOME"]
# TEST_MODE = os.environ.get("TEST_MODE", 0)
#
# if TEST_MODE:
#     DB_DIR = f"{DEMO_HOME}/db/test_dbs"
# else:
#     DB_DIR = f"{DEMO_HOME}/db"
#
# BADGES_COLLECTION = f"{DB_DIR}/badges.json"
# USER_COLLECTION = f"{DB_DIR}/users.json"
# TRAININGS_COLLECTION = f"{DB_DIR}/trainings.json"

# def write_collection(perm_version, mem_version):
#     """
#     Write out the in-memory data collection in proper DB format.
#     """
#     with open(perm_version, 'w') as f:
#         json.dump(mem_version, f, indent=4)
#
#
# def read_collection(perm_version):
#     """
#     A function to read a colleciton off of disk.
#     """
#     print(f"{perm_version=}")
#     try:
#         with open(perm_version) as file:
#             return json.loads(file.read())
#     except FileNotFoundError:
#         print(f"{perm_version} not found.")
#         return None
client = dbc.get_client()


if client is None:
    print("Failed to connect to MongoDB")
    exit(1)


def parse_json(data):
    return json.loads(json_util.dumps(data))


def get_users():
    """
    A function to return all users.
    """
    return dbc.fetch_all(USERS, NETID)


def get_password(username):
    """
    A function to return password param of user.
    """
    rec = dbc.fetch_one(USERS, filters={USERS_NM: username})
    data = parse_json(rec)
    return data['password']


def get_trainings():
    """
    A function to return a dictionary of all trainings.
    """
    # return read_collection(TRAININGS_COLLECTION)
    return dbc.fetch_all(TRAININGS, TRAININGS_NM)


def get_badges():
    """
    A function to return a dictionary of all badgenames and their description.
    """
    # return read_collection(BADGES_COLLECTION)
    # return dbc.fetch_all(BADGES, BADGES_NM)
    return dbc.fetch_all(BADGES, BADGES_NM, filters={})


def get_badge_by_id(badgename):
    """
    Get a specific badge by badgename from the db.
    Returns True or False
    """
    rec = dbc.fetch_one(BADGES, filters={BADGES_NM: badgename})
    return parse_json(rec)


def get_workshops():
    """
    A function to return a dictionary of all workshops.
    """

    # return read_collection(WORKSHOPS_COLLECTION)
    return dbc.fetch_all(WORKSHOPS, WORKSHOPS_NM)


def netid_exists(netid):
    """
    See if a user with username is in the db.
    Returns True or False
    """
    rec = dbc.fetch_one(USERS, filters={NETID: netid})
    return rec is not None


def workshop_exists(workshopname):
    """
    See if a workshop with workshopname is in the db.
    Returns True or False
    """
    rec = dbc.fetch_one(WORKSHOPS, filters={WORKSHOPS_NM: workshopname})
    return rec is not None


def badge_exists(badgename):
    """
    See if a user with username is in the db.
    Returns True or False
    """
    rec = dbc.fetch_one(BADGES, filters={BADGES_NM: badgename})
    return rec is not None


def training_exists(trainingname):
    """
    See if a training with trainingname is in the db.
    Returns True or False
    """
    rec = dbc.fetch_one(TRAININGS, filters={TRAININGS_NM: trainingname})
    return rec is not None


def add_user(netid, firstname, lastname, barcode=999999999):
    """
    Add a new user to the user database.
    """
    if netid_exists(netid):
        return DUPLICATE
    else:
        dbc.insert_doc(USERS, {NETID: netid, FIRST_NM: firstname,
                       LAST_NM: lastname, BARCODE: barcode})


# def add_user(username, password):
#     """
#     Add a new user to the user database.
#     """
#     if netid_exists(username):
#         return DUPLICATE
#     else:
#         dbc.insert_doc(USERS, {USERS_NM: username, PASSWORD: password})


def add_workshop(workshopname):
    """
    Add a new workshop to the workshop database.
    """
    if workshop_exists(workshopname):
        return DUPLICATE
    else:
        dbc.insert_doc(WORKSHOPS, {WORKSHOPS_NM: workshopname})


def add_badge(badgename, desc):
    """
    Add a new badge to the badge database.
    """
    if badge_exists(badgename):
        return DUPLICATE
    else:
        dbc.insert_doc(BADGES, {BADGES_NM: badgename}, filters={DESC: desc})


def add_training(trainingname):
    """
    Add a new training to the training database.
    """
    if training_exists(trainingname):
        return DUPLICATE
    else:
        dbc.insert_doc(TRAININGS, {TRAININGS_NM: trainingname})


def del_user(netid):
    """
    Delete username from the db.
    """
    if not netid_exists(netid):
        return NOT_FOUND
    else:
        dbc.del_one(USERS, filters={NETID: netid})
        return OK


def del_workshop(workshopname):
    """
    Delete workshop from the db.
    """
    if not workshop_exists(workshopname):
        return NOT_FOUND
    else:
        dbc.del_one(WORKSHOPS, filters={WORKSHOPS_NM: workshopname})
        return OK


def del_training(trainingname):
    """
    Delete training from the db.
    """
    if not training_exists(trainingname):
        return NOT_FOUND
    else:
        dbc.del_one(TRAININGS, filters={TRAININGS_NM: trainingname})
        return OK


def update_user(oldnetid, newnetid):
    """
    Update old user name in db with new user name.
    """
    if not netid_exists(oldnetid):
        return NOT_FOUND
    elif netid_exists(newnetid):
        return DUPLICATE
    else:
        dbc.update_one(USERS, filters={NETID: oldnetid},
                       updates={"$set": {NETID: newnetid}})
    return OK


def update_training(oldtrainingname, newtrainingname):
    """
    Update old training name in db with new training name.
    """
    if not training_exists(oldtrainingname):
        return NOT_FOUND
    elif training_exists(newtrainingname):
        return DUPLICATE
    else:
        dbc.update_one(TRAININGS, filters={TRAININGS_NM: oldtrainingname},
                       updates={"$set": {TRAININGS_NM: newtrainingname}})
    return OK


def update_badge(oldbadgename, newbadgename):
    """
    Update old badge name in db with new badge name.
    """
    if not badge_exists(oldbadgename):
        return NOT_FOUND
    elif badge_exists(newbadgename):
        return DUPLICATE
    else:
        dbc.update_one(BADGES, filters={BADGES_NM: oldbadgename},
                       updates={"$set": {BADGES_NM: newbadgename}})
    return OK


def update_badge_desc(badgename, newbadgedesc):
    """
    Update old badge description in db with new badge description.
    """
    if not badge_exists(badgename):
        return NOT_FOUND
    elif badge_exists(badgename):
        return DUPLICATE
    else:
        dbc.update_one(BADGES, filters={BADGES_NM: badgename},
                       updates={"$set": {DESC: newbadgedesc}})
    return OK


def update_workshop(oldwsname, newwsname):
    """
    Update old training name in db with new training name.
    """
    if not workshop_exists(oldwsname):
        return NOT_FOUND
    elif workshop_exists(newwsname):
        return DUPLICATE
    else:
        dbc.update_one(WORKSHOPS, filters={WORKSHOPS_NM: oldwsname},
                       updates={"$set": {WORKSHOPS_NM: newwsname}})
    return OK


def del_badge(badgename):
    """
    Delete badge from the db.
    """
    if not badge_exists(badgename):
        return NOT_FOUND
    else:
        # b, desc = get_badges()
        dbc.del_one(BADGES, filters={BADGES_NM: badgename})
        return OK
