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

    def test_create_badges(self):
        """
        Post-condition: return is a dictionary.
        """
        cr = ep.CreateBadges(Resource)
        new_badge = new_entity_name("badge")
        ret = cr.post(new_badge)
        badges = db.get_badges()
        self.assertIn(new_badge, badges)

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

    def test_delete_workshop(self):
        de = ep.DeleteWorkshop(Resource)
        delete_workshop = new_entity_name("workshop")
        cr = ep.CreateWorkshops(Resource)
        cr.post(delete_workshop)

        ret = de.post(delete_workshop)
        workshops = db.get_workshops()
        self.assertNotIn(delete_workshop,workshops)

    def test_delete_user(self):
        de = ep.DeleteUser(Resource)
        delete_user = new_entity_name("user")
        cr = ep.CreateUser(Resource)
        cr.post(delete_user)

        ret = de.delete(delete_user)
        users = db.get_users()
        self.assertNotIn(delete_user,users)

    def test_update_training(self):
        ut = ep.UpdateTrainings(Resource)
        old_training = new_entity_name("trainingtoupdate")
        new_training = new_entity_name("updatedtraining")
        cr = ep.CreateTrainings(Resource)
        cr.post(old_training)

        ret = ut.put(old_training, new_training)
        trainings = db.get_trainings()
        self.assertIn(new_training, trainings)

    def test_update_user(self):
        uu = ep.UpdateUser(Resource)
        old_user = new_entity_name("usertoupdate")
        new_user = new_entity_name("updateduser")
        cr = ep.CreateUser(Resource)
        cr.post(old_user)

        ret = uu.put(old_user, new_user)
        users = db.get_users()
        self.assertIn(new_user, users)
        self.assertNotIn(old_user, users)

    def test_update_badge(self):
        update_b = ep.UpdateBadges(Resource)
        old_b = new_entity_name("badgeupdate")
        new_b = new_entity_name("updatedbadge")
        cr = ep.CreateBadges(Resource)
        cr.post(old_b)

        ret = update_b.put(old_b, new_b)
        badges = db.get_badges()
        self.assertIn(new_b, badges)
        self.assertNotIn(old_b, badges)


    def test_update_workshop(self):
        update_ws = ep.UpdateWorkshops(Resource)
        old_ws = new_entity_name("workshopupdate")
        new_ws = new_entity_name("updatedworkshop")
        cr = ep.CreateWorkshops(Resource)
        cr.post(old_ws)

        ret = update_ws.put(old_ws, new_ws)
        workshops = db.get_workshops()
        self.assertIn(new_ws, workshops)
        self.assertNotIn(old_ws, workshops)