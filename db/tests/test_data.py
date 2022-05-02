"""
This file holds the tests for data.py.
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
        #user
        self.test_user_id = new_entity_name('user')
        db.add_user(self.test_user_id, "first", "last", "9999999")
        #badge
        self.test_badge_id = new_entity_name('badge')
        db.add_badge(self.test_badge_id, "test_description")
        #workshop
        self.test_workshop_id = new_entity_name('workshop')
        db.add_workshop(self.test_workshop_id)
        #training
        self.test_training_id = new_entity_name('training')
        db.add_training(self.test_training_id)

    def tearDown(self):
        db.del_user(self.test_user_id)
        db.del_badge(self.test_badge_id)
        db.del_workshop(self.test_workshop_id)
        db.del_training(self.test_training_id)

    def test_get_users(self):
        users = db.get_users()
        self.assertIsInstance(users, dict)
        self.assertIn(self.test_user_id, users)

    def test_get_badges(self):
        badges = db.get_badges()
        self.assertIsInstance(badges, dict)
        self.assertIn(self.test_badge_id, badges)
    
    def test_get_workshops(self):
        workshops = db.get_workshops()
        self.assertIsInstance(workshops, dict)
        self.assertIn(self.test_workshop_id, workshops)

    def test_get_trainings(self):
        trainings = db.get_trainings()
        self.assertIsInstance(trainings, dict)
        self.assertIn(self.test_training_id, trainings) 
