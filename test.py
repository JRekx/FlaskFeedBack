import unittest
from app import app, db
from models import User, Feedback
from forms import RegisterF, LoginF, FeedbackF

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        """Set up test app and database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback-test'
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """Clean up after tests."""
        with app.app_context():
            db.session.rollback()
            db.drop_all()

    def register_user(self):
        """Helper method to register a test user."""
        response = self.client.post('/register', data={
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }, follow_redirects=True)
        return response

    def test_homepage_redirect(self):
        """Test homepage redirects to /register."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/register')

    def test_register_user(self):
        """Test user registration."""
        response = self.register_user()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, testuser!', response.data)

    def test_login_user(self):
        """Test user login."""
        self.register_user()
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back, testuser!', response.data)

    def test_user_profile(self):
        """Test user profile page."""
        self.register_user()
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/users/testuser')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User Profile - testuser', response.data)

    def test_feedback_submission(self):
        """Test feedback submission."""
        self.register_user()
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/users/testuser/feedback/add')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/users/testuser/feedback/add', data={
            'title': 'Test Feedback',
            'content': 'This is a test feedback.'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Thanks for your feedback!', response.data)

    # Add more test cases as needed for other routes, forms, and functionality

if __name__ == '__main__':
    unittest.main()
