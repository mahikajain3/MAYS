"""
This file holds the tests for endpoints.py.
"""

from unittest import TestCase, skip
from flask_restx import Resource, Api

import API.endpoints as ep
import db.data as db
import random

HUGE_NUM = 10000000000000


def new_entity_name(entity_type):
    """
    Randomly create entity name for test
    """
    int_name = random.randint(0, HUGE_NUM)
    return f"new {entity_type}" + str(int_name)


class EndpointTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_hello(self):
        hello = ep.HelloWorld(Resource)
        ret = hello.get()
        self.assertIsInstance(ret, dict)
        self.assertIn(ep.HELLO, ret)

    def test_create_user(self):
        """
        Post-condition: return is a dictionary.
        """
        cr = ep.CreateUser(Resource)
        new_user = new_entity_name("user")
        ret = cr.post(new_user)
        users = db.get_users()
        self.assertIn(new_user, users)

    def test_create_workshops(self):
        """
        Post-condition: return is a dictionary.
        """
        cr = ep.CreateWorkshops(Resource)
        new_workshop = new_entity_name("workshop")
        ret = cr.post(new_workshop)
        workshops = db.get_workshops()
        self.assertIn(new_workshop, workshops)

    def test_list_user1(self):
        """
        Post-condition 1: return is a dictionary.
        """
        lr = ep.ListUsers(Resource)
        ret = lr.get()
        self.assertIsInstance(ret, dict)

    def test_list_users2(self):
        """
        Post-condition 2: keys to the dict are strings
        """
        lr = ep.ListUsers(Resource)
        ret = lr.get()
        for key in ret:
            self.assertIsInstance(key, str)

    def test_list_users3(self):
        """
        Post-condition 3: the values in the dict are themselves dicts
        """
        lr = ep.ListUsers(Resource)
        ret = lr.get()
        for val in ret.values():
            self.assertIsInstance(val, dict)

    def test_list_badges1(self):
        """
        Post-condition 1: return is a dictionary.
        """
        lr = ep.ListBadges(Resource)
        ret = lr.get()
        self.assertIsInstance(ret, dict)

    def test_list_badges2(self):
        """
        Post-condition 2: keys to the dict are strings
        """
        lr = ep.ListBadges(Resource)
        ret = lr.get()
        for key in ret:
            self.assertIsInstance(key, str)

    def test_list_badges3(self):
        """
        Post-condition 3: the values in the dict are themselves dicts
        """
        lr = ep.ListBadges(Resource)
        ret = lr.get()
        for val in ret.values():
            self.assertIsInstance(val, dict)

    def test_list_trainings1(self):
        """
        Post-condition 1: return is a dictionary.
        """
        lr = ep.ListTrainings(Resource)
        ret = lr.get()
        self.assertIsInstance(ret, dict)

    def test_list_trainings2(self):
        """
        Post-condition 2: keys to the dict are strings
        """
        lr = ep.ListTrainings(Resource)
        ret = lr.get()
        for key in ret:
            self.assertIsInstance(key, str)

    def test_list_trainings3(self):
        """
        Post-condition 3: the values in the dict are themselves dicts
        """
        lr = ep.ListTrainings(Resource)
        ret = lr.get()
        for val in ret.values():
            self.assertIsInstance(val, dict)

    def test_list_workshops1(self):
        """
        Post-condition 1: return is a dictionary.
        """
        lr = ep.ListWorkshops(Resource)
        ret = lr.get()
        self.assertIsInstance(ret, dict)

    def test_list_workshops2(self):
        """
        Post-condition 2: keys to the dict are strings
        """
        lr = ep.ListWorkshops(Resource)
        ret = lr.get()
        for key in ret:
            self.assertIsInstance(key, str)

    def test_list_workshops3(self):
        """
        Post-condition 3: the values in the dict are themselves dicts
        """
        lr = ep.ListWorkshops(Resource)
        ret = lr.get()
        for val in ret.values():
            self.assertIsInstance(val, dict)

    def test_delete_user(self):
        de = ep.DeleteUser(Resource)
        delete_user = new_entity_name("user")
        cr = ep.CreateUser(Resource)
        cr.post(delete_user)

        ret = de.post(delete_user)
        users = db.get_users()
        self.assertNotIn(delete_user,users)