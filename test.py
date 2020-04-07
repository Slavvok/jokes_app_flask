from app import create_app, db
from app.models import User
import unittest
from config import TestConfig
from app.views import auth, jokes


class JokesAppTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app(TestConfig)
        app.register_blueprint(auth.auth, url_prefix='/auth')
        app.register_blueprint(jokes.jokes)
        self.app = app.test_client()
        app.app_context().push()
        db.create_all()
        u = User('test', 'test@test.test')
        u.generate_hash('testtest')
        db.session.add(u)
        db.session.commit()
        self.login()
        self.generate_joke()
        # db.session.commit()
        # user = db.session.query(User).filter_by(name='test').first()

    def tearDown(self):
        db.drop_all()

    def login(self):
        return self.app.post('/auth/login', data=dict(
            username='test',
            password='testtest'
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/auth/logout', follow_redirects=True)

    def generate_joke(self):
        return self.app.post('/generate-joke')

    def test_registration(self):
        reg1 = self.app.post('/auth/registration', data=dict(
            username='test_new',
            password='testtest',
            email='test_new@test.test'
        ))
        self.assertEqual(reg1.status_code, 201)
        reg2 = self.app.post('/auth/registration', data=dict(
            username='test_new',
            password='testtest',
            email='test_new@test.test'
        ))
        self.assertEqual(reg2.status_code, 403)

    def test_logout_login(self):
        logout = self.logout()
        self.assertEqual(logout.status_code, 401)
        login = self.login()
        self.assertEqual(login.status_code, 200)

    def test_generate_joke(self):
        client = self.generate_joke()
        self.assertEqual(client.status_code, 201)

    def test_get_jokes_list(self):
        client = self.app.get('/get-jokes-list')
        self.assertEqual(client.status_code, 200)

    def test_get_joke(self):
        client = self.app.get('/get-joke/1')
        self.assertEqual(client.status_code, 200)

    def test_update_joke(self):
        client = self.app.put('/update-joke/1', data=dict(
            joke='Updated joke, even funnier'
        ))
        self.assertEqual(client.status_code, 201)

    def test_remove_joke(self):
        client = self.app.post('/remove-joke/1')
        self.assertEqual(client.status_code, 200)


if __name__ == '__main__':
    unittest.main()
