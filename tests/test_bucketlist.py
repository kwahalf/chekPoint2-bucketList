# test_bucketlist.py
import unittest
import os
import json
from app import create_app, db


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Go to Borabora for vacation'}
        self.bucketitem = {'name': 'Eat pawpaw'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def register_user(self, email="user@test.com", password="test1234"):
        """This helper method helps register a test user."""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('auth/register', data=json.dumps(user_data),
                               headers = {'content-type': 'application/json'})

    def login_user(self, email="user@test.com", password="test1234"):
        """This helper method helps log in a test user."""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=json.dumps(user_data),
                               headers = {'content-type': 'application/json'})

    def test_bucketlist_creation(self):
        """Test API can create a bucketlist (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data)['access_token']

        # create a bucketlist by making a POST request
        res = self.client().post(
            '/bucketlists/',
            headers = {'content-type': 'application/json',
             'Authorization': access_token}, data=json.dumps(self.bucketlist))
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go to Borabora for vacation', str(res.data))

    def test_api_can_get_all_bucketlists(self):
        """Test API can get a bucketlist (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data)['access_token']

        # create a bucketlist by making a POST request
        res = self.client().post(
            '/bucketlists/',
            headers = {'content-type': 'application/json',
             'Authorization': access_token}, data=json.dumps(self.bucketlist))
        self.assertEqual(res.status_code, 201)

        # get all the bucketlists that belong to the test user by making a GET request
        res = self.client().get(
            '/bucketlists/',
            headers = {'Authorization': access_token},
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to Borabora', str(res.data))

    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get a single bucketlist by using it's id."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # create a bucketlist by making a POST request
        res = self.client().post(
            '/bucketlists/',
            headers = {'content-type': 'application/json',
             'Authorization': access_token}, data=json.dumps(self.bucketlist))
        # assert that the bucketlist is created
        self.assertEqual(res.status_code, 201)

        # Get bucketlist by ID
        result = self.client().get(
            '/bucketlists/1',
            headers = {'content-type': 'application/json',
             'Authorization': access_token})
        # assert that the bucketlist is actually returned given its ID
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to Borabora', str(result.data))

    def test_bucketlist_can_be_edited(self):
        """Test API can edit an existing bucketlist. (PUT request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # first, we create a bucketlist by making a POST request
        rv = self.client().post(
            '/bucketlists/',
            headers = {'content-type': 'application/json',
             'Authorization': access_token},
             data=json.dumps({'name': 'Eat, pray and love'}))
        self.assertEqual(rv.status_code, 201)

        # then, we edit the created bucketlist by making a PUT request
        rv = self.client().put(
            '/bucketlists/1',
            headers = {'content-type': 'application/json',
             'Authorization': access_token},
            data= json.dumps({
                "name": "Dont just eat, but also pray and love :-)"
            }))
        self.assertEqual(rv.status_code, 200)

        # finally, we get the edited bucketlist to see if it is actually edited.
        results = self.client().get(
            '/bucketlists/1',
            headers = {'content-type': 'application/json',
             'Authorization': access_token})
        self.assertIn('Dont just eat', str(results.data))

    def test_bucketlist_deletion(self):
        """Test API can delete an existing bucketlist. (DELETE request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # create a bucketlist by making a POST request
        res = self.client().post(
            '/bucketlists/',
            headers = {'content-type': 'application/json',
             'Authorization': access_token}, data=json.dumps(self.bucketlist))
        # assert that the bucketlist is created
        self.assertEqual(res.status_code, 201)

        # delete the bucketlist we just created
        res = self.client().delete(
            '/bucketlists/1',
            headers = {'content-type': 'application/json',
             'Authorization': access_token},)
        self.assertEqual(res.status_code, 200)

        # Test to see if it exists, should return a 404
        result = self.client().get(
            '/bucketlists/1',
            headers = {'content-type': 'application/json',
             'Authorization': access_token})
        self.assertEqual(result.status_code, 404)

    def test_bucketitem_creation(self):
        """Test API can create a bucketitem (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data)['access_token']

        # create a bucketlist by making a POST request
        res = self.client().post(
            '/bucketlists/',
            headers = {'content-type': 'application/json',
             'Authorization': access_token}, data=json.dumps(self.bucketlist))
        self.assertEqual(res.status_code, 201)

        # create a bucketitem by making a POST request
        res = self.client().post(
            '/bucketlists/1/items/',
            headers = {'content-type': 'application/json',
             'Authorization': access_token}, data=json.dumps(self.bucketitem))
        self.assertEqual(res.status_code, 201)
        self.assertIn('Eat pawpaw', str(res.data))

    def test_bucketitem_can_be_edited(self):
        """Test API can edit an existing bucketlist. (PUT request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # create a bucketlist by making a POST request
        res = self.client().post(
            '/bucketlists/',
            headers = {'content-type': 'application/json',
             'Authorization': access_token}, data=json.dumps(self.bucketlist))
        # assert that the bucketlist is created
        self.assertEqual(res.status_code, 201)

        # create a bucketitem by making a POST request
        res = self.client().post(
            '/bucketlists/1/items/',
            headers = {'content-type': 'application/json',
             'Authorization': access_token}, data=json.dumps(self.bucketitem))
        self.assertEqual(res.status_code, 201)

        # then, we edit the created bucketitem by making a PUT request
        rv = self.client().put(
            '/bucketlists/1/items/1',
            headers = {'content-type': 'application/json',
             'Authorization': access_token},
            data= json.dumps({
                'name': 'Eat mangos too :-)', 'done': False
            }))
        self.assertEqual(rv.status_code, 200)

        # finally, we get the edited bucketlist to see if it is actually edited.
        results = self.client().get(
            '/bucketlists/1',
            headers = {'content-type': 'application/json',
             'Authorization': access_token})
        self.assertIn('Eat mangos too :-)', str(results.data))

    def test_bucketitem_deletion(self):
        """Test API can delete an existing bucketitem. (DELETE request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # create a bucketlist by making a POST request
        res = self.client().post(
            '/bucketlists/',
            headers = {'content-type': 'application/json',
             'Authorization': access_token}, data=json.dumps(self.bucketlist))
        # assert that the bucketlist is created
        self.assertEqual(res.status_code, 201)

        # create a bucketitem by making a POST request
        res = self.client().post(
            '/bucketlists/1/items/',
            headers = {'content-type': 'application/json',
             'Authorization': access_token}, data=json.dumps(self.bucketitem))
        self.assertEqual(res.status_code, 201)

        # delete the bucketitem we just created
        res = self.client().delete(
            '/bucketlists/1/items/1',
            headers = {'content-type': 'application/json',
             'Authorization': access_token},)
        self.assertEqual(res.status_code, 200)

        # Test to see if it exists, should not exist in bucketlist items
        results = self.client().get(
            '/bucketlists/1',
            headers = {'content-type': 'application/json',
             'Authorization': access_token})
        self.assertNotIn('Eat mangos too :-)', str(results.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
