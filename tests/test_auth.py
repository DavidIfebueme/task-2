import unittest
import json
from app import create_app, db
from app.models import User, Organisation, UserOrganisation

# Tests
# registering user successfully with default org
# log user in successfully
# failure if required fields are missing
# failure if !unique email or userId


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user_successfully(self):
        user_data = {
            "userId": "test_user_21",
            "firstName": "mentor",
            "lastName": "shully",
            "email": "mentorshully21@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client().post('/auth/register', data=json.dumps(user_data), content_type='application/json')
        result = json.loads(response.data)

        #assertion time :-)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['data']['user']['firstName'], 'mentor')
        self.assertIn('accessToken', result['data'])
        self.assertEqual(result['data']['user']['email'], 'mentorshully21@example.com')

    def test_login_user_successfully(self):
        user_data = {
            "userId": "test_user_22",
            "firstName": "mentor",
            "lastName": "shully",
            "email": "mentorshully22@example.com",
            "password": "password123",
            "phone": "1234"
        }
        self.client().post('/auth/register', data=json.dumps(user_data), content_type='application/json')
        login_data = {
            "email": "mentorshully22@example.com",
            "password": "password123"
        }
        response = self.client().post('/auth/login', data=json.dumps(login_data), content_type='application/json')
        result = json.loads(response.data)

        # assertion time again :-)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['status'], 'success')
        self.assertIn('accessToken', result['data'])

    def test_fail_if_required_fields_missing(self):
        user_data = {
            "userId": "test_user_23",
            "firstName": "mentor",
            "lastName": "",
            "email": "mentorshully23@example.com",
            "password": "password123",
            "phone": "1234"
        }
        response = self.client().post('/auth/register', data=json.dumps(user_data), content_type='application/json')
        result = json.loads(response.data)

        #assertions dey sweet walai
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result['errors'][0]['field'], 'lastName')

    def test_fail_if_duplicate_email_or_userid(self):
        user_data_1 = {
            "userId": "test_user_24",
            "firstName": "mentor",
            "lastName": "shully",
            "email": "mentorshully24@example.com",
            "password": "password123",
            "phone": "23679744294"
        }
        user_data_2 = {
            "userId": "test_user_25",
            "firstName": "myback",
            "lastName": "ispainingme",
            "email": "mentorshully24@example.com",  # Duplicate mentorshully email
            "password": "password123",
            "phone": "27362967233"
        }
        self.client().post('/auth/register', data=json.dumps(user_data_1), content_type='application/json')
        response = self.client().post('/auth/register', data=json.dumps(user_data_2), content_type='application/json')
        result = json.loads(response.data)

        #if i no assert wetin i gain
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result['errors'][0]['field'], 'email')

if __name__ == "__main__":
    unittest.main()
