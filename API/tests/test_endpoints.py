"""
This file holds the tests for endpoints.py.
"""

from unittest import TestCase, skip
from flask_restx import Resource, Api

import API.endpoints as ep
import db.db as db
import random


HUGE_NUM = 10000000000000

def new_user_name():
	int_name = random.randint(0, HUGE_NUM)	
	return "new user" + str(int_name)

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
		new_user = new_user_name()
		ret = cr.post(new_user)
		users = db.get_users()
		self.assertIn(new_user, users)

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
