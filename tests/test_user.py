from models.common import User
from models.common import Base
from sqlalchemy_utils.types import Password
from unittest import TestCase
from . import testdb


class TestUser(TestCase):
    def setUp(self):
        engine, self.session = testdb()
        Base.metadata.create_all(engine)

        self.username = 'regular'
        self.password = '1234'

        self.user = User(username=self.username, password=self.password)
        self.session.add(self.user)
        self.session.commit()

    def test_login_correct_credentials_returns_truthy(self):
        self.assertTrue(User.login(self.username, self.password, self.session))

    def test_login_with_incorrect_username_returns_falsey(self):
        self.assertFalse(User.login(self.username + 'x', self.password, self.session))

    def test_login_with_incorrect_password_returns_falsey(self):
        self.assertFalse(User.login(self.username, self.password + 'x', self.session))

    def test_password_is_not_plain_text_returns_falsey(self):
        self.assertIsInstance(self.user.password, Password)

    def test_login_correct_returns_user_instance(self):
        self.assertIsInstance(User.login(self.username, self.password, self.session), User)
