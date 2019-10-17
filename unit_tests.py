import unittest
import json
from copy import deepcopy

import app


BASE_URL = 'http://127.0.0.1:5000'

class Testapp(unittest.TestCase):

    def setUp(self):
        self.backup_items = deepcopy(app.items) # recursively makes a copy of each element
        self.client = app.app.test_client() # returns a new instance of the app in test_mode
        self.client.testing = True

    def test_date(self):
        """No JSON Request"""

        response = self.client.get(f'{BASE_URL}/dates')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data.keys()), 3)
        # weekday should not be in data
        self.assertFalse("weekday" in data)

    def test_valid_keys(self):
        """Valid fields. Should return 200"""
        
        passing_in_json = {"full":True}
        response = self.client.get(f'{BASE_URL}/dates',
                        
                                    data=json.dumps(passing_in_json), 
                                    content_type='application/json')
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("weekday" in data)
    
    def test_bad_key(self):
        """Bad key JSON request. Should return 400"""
        
        passing_in_json = {"wrong_key": "etx"}
        response = self.client.get(f'{BASE_URL}/dates',
                                data=json.dumps(passing_in_json), 
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    
    def test_bad_value(self):
        """Bad value JSON request. Should return 400"""

        passing_in_json = {"full": "etx"}
        response = self.client.get(f'{BASE_URL}/dates',
                                data=json.dumps(passing_in_json), 
                                content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_bad_post(self):
        """Missing Fields. Should return 400"""
        passing_in_json = {"name":"desk"}

        response = self.client.post(f'{BASE_URL}/items',
                                    data=json.dumps(passing_in_json),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_invalid_type_post(self):
        """ "Value" field cannot take str. Should only accept int. Return 400"""

        passing_in_json = {"name":"desk", "value":"this is an int"}
        response = self.client.post(f'{BASE_URL}/items',
                                    data=json.dumps(passing_in_json),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_good_post(self):
        """Valid. Both name and value are correct types"""

        passing_in_json = {"name":"flowers", "value":2031}

        response = self.client.post(f'{BASE_URL}/items',
                                    data=json.dumps(passing_in_json),
                                    content_type='application/json')

        data = json.loads(response.get_data())
        self.assertEqual(data['new_item']['name'], 'flowers')
        self.assertEqual(data['new_item']['value'], 2031)
    
    def test_put(self):
        """Update the value of id:1 """

        passing_in_json = {"value": 30}

        response = self.client.put(f'{BASE_URL}/items/1',
                                    data=json.dumps(passing_in_json),
                                    content_type='application/json')

        data = json.loads(response.data) 
        self.assertEqual(data['updated_item']['value'], 30)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.backup_items[0]['value'], 1000) 


    def tearDown(self):
        # reset app.items to initial state
        app.items = self.backup_items




if __name__ == '__main__':
    unittest.main()