"""
This file holds the tests for endpoints.py.
"""

from flask import Flask
from unittest import TestCase, skip
from flask_restx import Resource, Api

import API.endpoints as ep
import db.data as db
import random

HUGE_NUM = 10000000000000

app = Flask(__name__)

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
        with app.test_request_context('/create/<netid>'):
            cr = ep.CreateUser(Resource)
            new_user = new_entity_name("user")
            ret = cr.post(new_user)
            users = db.get_users()
        assert new_user in users

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
        with app.test_request_context('/create/<badgename>'):
            cr = ep.CreateBadges(Resource)
            new_badge = new_entity_name("badge")
            ret = cr.post(new_badge)
            badges = db.get_badges()
        assert new_badge in badges

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

    # def test_list_trainings2(self):
    #     """
    #     Post-condition 2: keys to the dict are strings
    #     """
    #     lr = ep.ListTrainings(Resource)
    #     ret = lr.get()
    #     for key in ret:
    #         self.assertIsInstance(key, str)

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

    # def test_list_workshops2(self):
    #     """
    #     Post-condition 2: keys to the dict are strings
    #     """
    #     lr = ep.ListWorkshops(Resource)
    #     ret = lr.get()
    #     for key in ret:
    #         self.assertIsInstance(key, str)

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

        ret = de.delete(delete_workshop)
        workshops = db.get_workshops()
        self.assertNotIn(delete_workshop,workshops)

    def test_delete_user(self):
        with app.test_request_context('/delete/<username>'):
            de = ep.DeleteUser(Resource)
            delete_user = new_entity_name("user")
            cr = ep.CreateUser(Resource)
            cr.post(delete_user)

            ret = de.delete(delete_user)
            users = db.get_users()
        assert delete_user not in users
    
    def test_delete_training(self):
        de = ep.DeleteTraining(Resource)
        delete_training = new_entity_name("training")
        cr = ep.CreateTrainings(Resource)
        cr.post(delete_training)

        ret = de.delete(delete_training)
        trainings = db.get_trainings()
        self.assertNotIn(delete_training,trainings)

    def test_delete_badge(self):
        with app.test_request_context('/delete/<badgename>'):
            de = ep.DeleteBadge(Resource)
            delete_badge = new_entity_name("badge")
            cr = ep.CreateBadges(Resource)
            cr.post(delete_badge)

            ret = de.delete(delete_badge)
            badges = db.get_badges()
        assert delete_badge not in badges

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
        with app.test_request_context('/update/<oldnetid>/<newnetid>'):
            uu = ep.UpdateUser(Resource)
            old_user = new_entity_name("usertoupdate")
            new_user = new_entity_name("updateduser")
            cr = ep.CreateUser(Resource)
            cr.post(old_user)

            ret = uu.put(old_user, new_user)
            users = db.get_users()
        assert new_user in users
        assert old_user not in users

    def test_update_badge(self):
        with app.test_request_context('/update/<oldbadgename>/<newbadgename>/<newdescription>'):
            update_b = ep.UpdateBadges(Resource)
            old_b = new_entity_name("badgeupdate")
            new_b = new_entity_name("updatedbadge")
            new_d = new_entity_name("")
            cr = ep.CreateBadges(Resource)
            cr.post(old_b)

            ret = update_b.put(old_b, new_b, new_d)
            badges = db.get_badges()
        assert new_b in badges
        assert old_b not in badges

    def test_update_badge_desc(self):
        with app.test_request_context('/update/<oldbadgename>/<newbadgename>/<newdescription>'):
            update_b = ep.UpdateBadges(Resource)
            old_b = new_entity_name("badgeupdate")
            new_b = new_entity_name("updatedbadge")
            new_d = new_entity_name("newdesc")
            cr = ep.CreateBadges(Resource)
            cr.post(old_b)

            ret = update_b.put(old_b, new_b, new_d)
            badges = db.get_badges()
        assert new_b in badges
        assert old_b not in badges

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


    def test_get_badge_by_id(self):
        """
        Post-condition 1: return is a dictionary.
        """
        with app.test_request_context('/list/<badgename>'):
            get_badge_by_id = ep.GetBadgesByID(Resource)
            badgename = new_entity_name("uniquebadge")
            cr = ep.CreateBadges(Resource)
            cr.post(badgename)

            ret = get_badge_by_id.get(badgename)
        assert type(ret) == dict