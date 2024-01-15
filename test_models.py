from unittest import TestCase
from app import app
from models import db, connect_db, User

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["TESTING"] = True


with app.app_context():
    db.drop_all()
    db.create_all()


class UserModelTest(TestCase):
    """Tests for User model"""

    def setUp(self):
        """Clear existing users"""

        self.app_context = app.app_context()
        self.app_context.push()

        User.query.delete()

        user = User(first_name="Caden", last_name="Carlson")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        self.app_context.pop()

    def test_show_user(self):
        with app.test_client() as client:
            res = client.get(f"/users/{self.user_id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Caden Carlson</h1>", html)