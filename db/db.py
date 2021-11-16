"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import json
import os

MAYS_HOME = os.environ["MAYS_HOME"]
TEST_MODE = os.environ.get("TEST_MODE", 0)
DB_DIR = f"{MAYS_HOME}/db"

if TEST_MODE:
    USERS_DB = f"{DB_DIR}/test_users.json"
else:
    USERS_DB = f"{DB_DIR}/users.json"

OK = 0
NOT_FOUND = 1
DUPLICATE = 2


def write_users(users):
    """
    Write new user name in json file (db).
    """
    with open(USERS_DB, 'w') as f:
        json.dump(users, f, indent=4)


def get_users():
    """
    A function to return all users.
    """
    try:
        with open(USERS_DB) as file:
            return json.loads(file.read())
    except FileNotFoundError:
        print("Users db not found")
        return None


def add_user(username):
    """
    Add a new user to the user database.
    Until we are using a real DB, we have a potential race condition.
    """
    users = get_users()
    if users is None:
        return NOT_FOUND
    elif username in users:
        return DUPLICATE
    else:
        users[username] = {"num_users": 0}
        write_users(users)
        return OK
