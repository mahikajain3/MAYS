"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import os

import db.db_connect as dbc

MAYS_HOME = os.environ["MAYS_HOME"]

# collection name
USERS = "users"
TRAININGS = "trainings"
BADGES = "badges"

# field names in our DB:
USER_NM = "userName"
TRAININGS_NM = "trainingName"
BADGES_NM = "badgeName"

OK = 0
NOT_FOUND = 1
DUPLICATE = 2

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


def get_trainings():
    """
    A function to return a dictionary of all users.
    """
    return dbc.fetch_all(TRAININGS, TRAININGS_NM)


def get_badges():
    """
    A function to return a dictionary of all users.
    """
    return dbc.fetch_all(BADGES, BADGES_NM)


def add_user(username):
    """
    Add a new user to the user database.
    """
    if user_exists(username):
        return DUPLICATE
    else:
        dbc.insert_doc(USERS, {USER_NM: username})


def del_user(username):
    """
    Delete username from the db.
    """
    if not user_exists(username):
        return NOT_FOUND
    else:
        dbc.del_one(USERS, filters={USER_NM: username})
        return OK
