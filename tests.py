from unittest import TestCase
from server import app
from model import connect_to_db, db
from flask import session

class FlaskTestsBasic(TestCase):
    """Basic flask route tests."""

    def setUp(self):

        self.client = app.test_client()
        app.config['Testing'] = True
    
    def test_index(self):
        """Test homepage."""

        result = self.client.get('/')
        self.assertIn(b"historical", result.data)
    
    # def test_login(self):
    #     """Test log-in route."""

    #     result = self.client.get('/log-in', 
    #                               data = {"email" : "user0@test.com", 'password' : "test"}, 
    #                               )
    #     self.assertIn(b"Logged In", result.data)

class FlaskTestsLoggedIn(TestCase):
    """Flask route tests with a user logged in."""

    def setUp(self):

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
    
    def favorite_trails(self):
        """Test favorite trails route when logged-in."""

        result = self.client.get('/favorite-trails')

        self.assertIn(b"Location", result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()