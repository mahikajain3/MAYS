"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import json
import os

MAYS_HOME = os.environ["MAYS_HOME"]
TEST_MODE = os.environ.get("TEST_MODE", 0)

if TEST_MODE:
    DB_DIR = f"{MAYS_HOME}/db/test_dbs"
else:
    DB_DIR = f"{MAYS_HOME}/db"

USER_COLLECTION = f"{DB_DIR}/users.json"

OK = 0
NOT_FOUND = 1
DUPLICATE = 2


# if os.environ.get("LOCAL_MONGO", False):
# else:
#    client = pm.MongoClient()
# print(client)

def write_collection(perm_version, mem_version):
    """
    Write out the in-memory data collection in proper DB format.
    """
    with open(perm_version, 'w') as f:
        json.dump(mem_version, f, indent=4)


def read_collection(perm_version):
    """
    A function to read a collection off of disk.
    """
    try:
        with open(perm_version) as file:
            return json.loads(file.read())
    except FileNotFoundError:
        print(f"{perm_version} not found.")
        return None


def get_users():
    """
    A function to return all users.
    """
    return read_collection(USER_COLLECTION)


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
        users[username] = {}
        write_collection(USER_COLLECTION, users)
        return OK
