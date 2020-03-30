from app import app
from app.model.center import Center
import unittest
import uuid
import json


class FlaskBookshelfTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_should_create_center(self):
        login = uuid.uuid4().hex
        password = uuid.uuid4().hex
        centers = self.app.get('/centers')
        self.assertEqual(centers.status_code, 200)
        json_data = centers.json
        self.assertTrue(len([x for x in json_data if login in x]) == 0)
        self.app.post("/register", data=json.dumps({
            "login": login,
            "password": password,
            "address": "Home, sweet home"
        }),
                      content_type='application/json')
        centers = self.app.get('/centers')
        self.assertEqual(centers.status_code, 200)
        json_data = centers.json
        center_list = [x for x in json_data if login in x]
        self.assertTrue(len(center_list) == 1)
        Center.remove(center_list[0].split()[-1])
