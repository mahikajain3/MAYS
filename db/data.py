"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import os
# import json

import db.db_connect as dbc

MAYS_HOME = os.environ["MAYS_HOME"]

# collection name
USERS = "users"
TRAININGS = "trainings"
BADGES = "badges"
WORKSHOPS = "workshops"

# field names in our DB:
USER_NM = "userName"
TRAININGS_NM = "trainingName"
BADGES_NM = "badgeName"
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


def get_users():
    """
    A function to return all users.
    """
    return dbc.fetch_all(USERS, USER_NM)


def user_exists(username):
    """
    See if a user with username is in the db.
    Returns True or False
    """
    rec = dbc.fetch_one(USERS, filters={USER_NM: username})
    return rec is not None


def workshop_exists(workshopname):
    """
    See if a user with username is in the db.
    Returns True or False
    """
    rec = dbc.fetch_one(WORKSHOPS, filters={WORKSHOPS_NM: workshopname})
    return rec is not None


def training_exists(trainingname):
    """
    See if a training with trainingname is in the db.
    Returns True or False
    """
    rec = dbc.fetch_one(TRAININGS, filters={TRAININGS_NM: trainingname})
    return rec is not None


def get_trainings():
    """
    A function to return a dictionary of all trainings.
    """
    # return read_collection(TRAININGS_COLLECTION)
    return dbc.fetch_all(TRAININGS, TRAININGS_NM)


def get_badges():
    """
    A function to return a dictionary of all badges.
    """
    # return read_collection(BADGES_COLLECTION)
    return dbc.fetch_all(BADGES, BADGES_NM)


def get_workshops():
    """
    A function to return a dictionary of all workshops.
    """

    # return read_collection(WORKSHOPS_COLLECTION)
    return dbc.fetch_all(WORKSHOPS, WORKSHOPS_NM)


def add_user(username):
    """
    Add a new user to the user database.
    """
    if user_exists(username):
        return DUPLICATE
    else:
        dbc.insert_doc(USERS, {USER_NM: username})


def add_workshop(workshopname):
    """
    Add a new workshop to the workshop database.
    """
    if workshop_exists(workshopname):
        return DUPLICATE
    else:
        dbc.insert_doc(WORKSHOPS, {WORKSHOPS_NM: workshopname})


def add_training(trainingname):
    """
    Add a new training to the training database.
    """
    if training_exists(trainingname):
        return DUPLICATE
    else:
        dbc.insert_doc(TRAININGS, {TRAININGS_NM: trainingname})


def del_user(username):
    """
    Delete username from the db.
    """
    if not user_exists(username):
        return NOT_FOUND
    else:
        dbc.del_one(USERS, filters={USER_NM: username})
        return OK
