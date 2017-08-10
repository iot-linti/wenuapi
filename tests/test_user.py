from sqlalchemy_utils.types import Password
import unittest
from __init__ import testdb
from ..wenuapi.models.common import Base
from ..wenuapi.models.user import User
from ..wenuapi.models.role import Role
from ..wenuapi.models.roletable import RoleTable

import time

class TestUser(unittest.TestCase):
    def setUp(self):
        engine, self.session = testdb()
        Base.metadata.create_all(engine)

        self.username = 'regular'
        self.password = '1234'
        self.rolename = 'admin'
        self.roleList = ['admin','user']
        self.token = User.generate_token(self.username)

        self.role = Role(rolename=self.rolename)
        self.user = User(username=self.username, password=self.password,token=self.token)
        self.user.roles.append(self.role)
        self.session.add(self.user)
        self.session.commit()


    '''
    #Test login with username and password
    '''
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

    '''
    #Test login with token
    '''
    def test_login_token_correct_credentials_returns_truthy(self):
        self.assertTrue(User.token_login(self.token, session = self.session))

    def test_token_login_with_incorrect_token_returns_falsey(self):
        self.assertFalse(User.token_login(self.token + 'x', session = self.session))

    '''
    #Test token expiration
    '''
    def test_token_login_with_expiration_returns_truthy(self):
        self.assertTrue(User.token_login(self.token, session = self.session))

    def test_token_login_with_expiration_returns_falsey(self):
        EXPIRES_IN_ONE_SECONDS = 1
        self.user.token = User.generate_token(self.username,EXPIRES_IN_ONE_SECONDS)
        self.session.query(User).filter(User.username == self.user.username).update({'token':self.user.token})
        self.session.commit()
        time.sleep(2)
        self.assertFalse(User.token_login(self.token, session = self.session))

    '''
    #Role test
    '''
    def test_is_admin_returns_truthy(self):
        self.assertTrue(self.user.isAdmin())

    def test_is_admin_returns_falsey(self):
        self.role.rolename = 'admino'
        self.assertFalse(self.user.isAdmin())

    def test_role_returns_truthy(self):
        self.assertTrue(self.user.isAuthorized(self.roleList))

    def test_role_returns_falsey(self):
        self.roleList.pop(0)
        self.assertFalse(self.user.isAuthorized(self.roleList))

if __name__ == '__main__':
    unittest.main()
