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
    return f"new{entity_type}" + str(int_name)


class EndpointTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_user(self):
        """
        Post-condition: return is a dictionary.
        """
        user_fields = {'firstname': ['firstname_test']}
        netid = new_entity_name('abc')
        response = ep.app.test_client().post(f'/users/create/{netid}', json=user_fields)
        self.assertEqual(response.status_code, 200)

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
        badge_fields = {'trainingname': ['trainingtest']}
        badge_nm = new_entity_name('badge')
        response = ep.app.test_client().post(f'/badges/create/{badge_nm}', json=badge_fields)
        self.assertEqual(response.status_code, 200)

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
        user_fields = {'firstname': ['firstname_test']}
        temp_netid = new_entity_name('abc')
        netid = db.add_user(temp_netid, "Mahika", "Jain", "9999999999")
        response = ep.app.test_client().delete(f'/users/delete/{temp_netid}', json=user_fields)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_training(self):
        de = ep.DeleteTraining(Resource)
        delete_training = new_entity_name("training")
        cr = ep.CreateTrainings(Resource)
        cr.post(delete_training)

        ret = de.delete(delete_training)
        trainings = db.get_trainings()
        self.assertNotIn(delete_training,trainings)

    def test_delete_badge(self):
        badge_fields = {'trainingname': ['trainingtest']}
        badge_nm = new_entity_name('badge')
        test = ep.app.test_client().post(f'/badges/create/{badge_nm}', json=badge_fields)
        response = ep.app.test_client().delete(f'/badges/delete/{badge_nm}', json=badge_fields)
        self.assertEqual(response.status_code, 200)

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
        user_fields = {'firstname': ['firstname_test']}
        old_netid = new_entity_name('abc')
        new_netid = new_entity_name('abc')
        netid = db.add_user(old_netid, "Mahika", "Jain", "99999999")
        response = ep.app.test_client().put(f'/users/update/{old_netid}/{new_netid}')
        self.assertEqual(response.status_code, 200)

    def test_update_badge(self):
        badge_fields = {'trainingname': ['trainingtest']}
        old_badge_nm = new_entity_name('badge')
        new_badge_nm = new_entity_name('badge')
        new_d = new_entity_name('desc')
        badge = db.add_badge(old_badge_nm, "")
        response = ep.app.test_client().put(f'/badges/update/{old_badge_nm}/{new_badge_nm}/{new_d}')
        self.assertEqual(response.status_code, 200)
        
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
        # with app.test_request_context('/list/<badgename>'):
        #     get_badge_by_id = ep.GetBadgesByID(Resource)
        #     badgename = new_entity_name("uniquebadge")
        #     cr = ep.CreateBadges(Resource)
        #     cr.post(badgename)
        #
        #     ret = get_badge_by_id.get(badgename)
        # assert type(ret) == dict
        badge_fields = {'badgename': ['badgetest']}
        badgename = new_entity_name('badge')
        response = ep.app.test_client().post(f'/badges/create/{badgename}', json=badge_fields)
        ret = ep.app.test_client().get(f'/badges/list/{badgename}')
        self.assertEqual(ret.status_code, 200)

    def test_get_user_by_id(self):
        """
        Post-condition 1: return is a dictionary.
        """
        user_fields = {'firstname': ['firstname_test']}
        netid = new_entity_name('abc')
        response = ep.app.test_client().post(f'/users/create/{netid}', json=user_fields)
        ret = ep.app.test_client().get(f'/users/list/{netid}')
        self.assertEqual(ret.status_code, 200)