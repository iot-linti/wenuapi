from .common import CommonColumns
from flask import current_app as app
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import relationship
from sqlalchemy_utils import PasswordType
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
)
import random,string


from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer
from itsdangerous import SignatureExpired, BadSignature

SECRET_KEY = 'this-is-my-super-secret-key'
default_expiration=24*60*60

def randomToken():
    return (''.join(random.choice(string.ascii_uppercase)for x in range(10)))

class User(CommonColumns):
    __tablename__ = 'user'
    _id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80),unique=True)
    password = Column(PasswordType(schemes=['pbkdf2_sha512']))
    token = Column(String(150),unique=True)
    #roles = relationship("Role", backref="users")
    roles = relationship('Role', secondary= 'roletable',backref='users')

    def isAdmin(self):
        """Checks if user is admin.
        """
        admin = ['admin']
        list = []
        for rol in self.roles:
            list.append(rol.rolename)
        cant = len(set(list).intersection(admin))

        return cant > 0

    def isAuthorized(self, role_names):
        """Checks if user is related to given role_names.
        """
        list = []
        for rol in self.roles:
            list.append(rol.rolename)
        cant = len(set(list).intersection(role_names))

        return cant > 0

    @staticmethod
    def generate_token(username,expiration=None):
        if expiration is None:
            expiration = default_expiration
        #print expiration
        s = Serializer(SECRET_KEY,expires_in=expiration)
        token = s.dumps({'login': username})
        return token


    @staticmethod
    def validate_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            print 'Expiro'
            return None # valid token, but expired
        except BadSignature:
            print 'Mala firma'
            return None # invalid token
        return data['login']

    @classmethod
    def token_login(cls, token, resource= None, method=None,allowed_roles = None ,session = None):

        if session is None:
            session = app.data.driver.session

        if User.validate_token(token):
            try:
                user = session.query(User).filter(User.token == token).one()
                if(allowed_roles and user.isAuthorized(allowed_roles) == 0):
                    user=None
            except NoResultFound:
                user = None
        else:
            user = None
        return user

    @classmethod
    def reset_token(cls, token, resource, method,allowed_roles = None ,session = None):

            if session is None:
                session = app.data.driver.session

            user = User.token_login(token,resource,method,session=session)

            if user:
                username = user.username
                new_token = User.generate_token(username)
                session.query(User).filter(User.username == username).update({'token':new_token})
                session.commit()

            return user

    @classmethod
    def login(cls, username, password, session=None):

        if session is None:
            session = app.data.driver.session
        try:
            user = session.query(User).filter(User.username == username).one()
        except NoResultFound:
            user = None
        else:
            token = User.generate_token(username)
            session.query(User).filter(User.username == user.username).update({'token':token})
            session.commit()
            user = user if user.password == password else None
        return user

    @classmethod
    def set_admin(cls, password, session=None):
        if session is None:
            session = app.data.driver.session

        user = None
        try:
            user = session.query(User).filter(User.username == 'admin').one()
        except NoResultFound:
            user = User(username='admin', password=password)
        else:
            user.password = password
        finally:
            if user is not None:
                user.token = User.generate_token('admin')
                session.add(user)
                session.commit()
        return user


