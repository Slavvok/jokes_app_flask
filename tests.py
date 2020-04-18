from app import create_app, db
from app.models import User
import unittest
from config import TestConfig
from app.views import auth, jokes
import json


class JokesAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app.app_context().push()
        self.app.register_blueprint(auth.auth, url_prefix='/auth')
        self.app.register_blueprint(jokes.jokes)
        self.db = db
        self.db.create_all()
        self.client = self.app.test_client()
        u = User('test', 'test@test.test')
        u.generate_hash('testtest')
        self.db.session.add(u)
        self.db.session.commit()
        self.auth_jwt()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def auth_jwt(self):
        response = self.client.post(
            '/auth/jwt',
            data=json.dumps(dict(
                username='test',
                password='testtest')),
            follow_redirects=True,
            headers={"Content-Type": "application/json"}).json
        self.access_token = response['access_token']
        self.refresh_token = response['refresh_token']
        self.headers = {"Content-Type": "application/json",
                        "Authorization": f"Bearer {self.access_token}"}

    # def logout(self):
    #     return self.client.get('/auth/logout', follow_redirects=True).json

    def test_registration(self):
        reg1 = self.client.post(
            '/auth/registration',
            data=json.dumps(dict(
                username='test_new',
                password='testtest',
                email='test_new@test.test'
            )),
            headers=self.headers)
        self.assertEqual(reg1.status_code, 201)
        reg2 = self.client.post(
            '/auth/registration',
            data=json.dumps(dict(
                username='test_new',
                password='testtest',
                email='test_new@test.test'
            )),
            headers=self.headers)
        self.assertEqual(reg2.status_code, 403)

    def test_generate_joke(self):
        response = self.client.post(
            '/generate-joke',
            headers=self.headers)
        self.assertEqual(response.status_code, 201)

    # def test_get_jokes_list(self):
        response = self.client.get('/get-jokes-list', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    # def test_get_joke(self):
        response = self.client.get('/get-joke/1', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    # def test_update_joke(self):
        response = self.client.put(
            '/update-joke/1',
            data=json.dumps(dict(
                joke='Updated joke, even funnier'
            )),
            headers=self.headers)
        self.assertEqual(response.status_code, 201)

    # def test_remove_joke(self):
        response = self.client.post('/remove-joke/1', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    # def test_logout_login(self):
    #     logout = self.logout()
    #     self.assertEqual(logout.status_code, 401)
    #     login = self.auth_jwt()
    #     self.assertEqual(login.status_code, 200)

    def test_refresh_token(self):
        response = self.client.post(
            'auth/refresh',
            headers={"Authorization": f"Bearer {self.refresh_token}"})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
