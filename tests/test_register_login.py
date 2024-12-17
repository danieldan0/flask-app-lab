import unittest
from app import create_app, db, bcrypt
from flask import session, url_for
from app.users.models import User

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("test")
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        
        hashed_password = bcrypt.generate_password_hash("password123").decode('utf-8')
        self.user = User(username="testing", email="test@example.com", password=hashed_password)
        db.session.add(self.user)
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_register_page_loads(self):
        response = self.client.get("/user/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Register", response.data)

    def test_login_page_loads(self):
        response = self.client.get("/user/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)
    
    def test_register_user(self):
        response = self.client.post("/user/register", data=dict(
            username="newuser",
            email="newuser@example.com",
            password="password123",
            confirm_password="password123"
        ))
        self.assertEqual(response.status_code, 302)
        
        user = User.query.filter_by(username="newuser").first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password("password123"))

    def test_login_user(self):
        response = self.client.post("/user/login", data=dict(
            email="test@example.com",
            password="password123"
        ))
        self.assertEqual(response.status_code, 302)

        with self.client:
            self.client.get("/")
            self.assertIn("_user_id", session)
    
    def test_logout_user(self):
        self.client.post("/user/login", data=dict(
            email="test@example.com",
            password="password123"
        ))
        response = self.client.get("/user/logout")
        self.assertEqual(response.status_code, 302)

        with self.client:
            self.client.get("/")
            self.assertNotIn("_user_id", session)


if __name__ == "__main__":
    unittest.main()