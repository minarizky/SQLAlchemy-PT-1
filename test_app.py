import unittest
from app import app, db, User

class BloglyTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'

        with app.app_context():
            db.create_all()
            user = User(first_name="Test", last_name="User", image_url=None)
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_user_listing(self):
        with self.client as c:
            resp = c.get('/users')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Test User', resp.data)

    def test_add_user(self):
        with self.client as c:
            resp = c.post('/users/new', data={'first_name': 'New', 'last_name': 'User', 'image_url': ''}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'New User', resp.data)

    def test_user_detail(self):
        with self.client as c:
            resp = c.get('/users/1')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Test User', resp.data)

    def test_edit_user(self):
        with self.client as c:
            resp = c.post('/users/1/edit', data={'first_name': 'Updated', 'last_name': 'User', 'image_url': ''}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Updated User', resp.data)

if __name__ == '__main__':
    unittest.main()
