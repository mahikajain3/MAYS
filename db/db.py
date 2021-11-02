"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import json
import os

MAYS_HOME = os.environ["MAYS_HOME"]

USERS_DB = f"{MAYS_HOME}/db/users.json"


def get_users():
    """
    A function to return all users.
    """
    try:
        with open(USERS_DB) as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return None
