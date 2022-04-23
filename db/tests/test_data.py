"""
This file holds the tests for endpoints.py.
"""

from unittest import TestCase, skip

import db.data as db
import random

HUGE_NUM = 10000000000000


def new_entity_name(entity_type):
    """
    Randomly create entity name for test
    """
    int_name = random.randint(0, HUGE_NUM)
    return f"new {entity_type}" + str(int_name)


class DataTestCase(TestCase):
    def setUp(self):
        self.test_user_id = new_entity_name('user')
        db.add_user(self.test_user_id, "first", "last", "9999999")

    def tearDown(self):
        db.del_user(self.test_user_id)

    def test_get_users(self):
        users = db.get_users()
        self.assertIsInstance(users, dict)
        self.assertIn(self.test_user_id, users)
    
