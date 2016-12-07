from .common import CommonColumns
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils import PasswordType
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
)

class User(CommonColumns):
    __tablename__ = 'user'
    _id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80))
    password = Column(PasswordType(schemes=['pbkdf2_sha512']))

    @classmethod
    def login(cls, username, password, session=None):
        try:
            user = session.query(User).filter(User.username == username).one()
        except NoResultFound:
            user = None
        else:
            user = user if user.password == password else None
        finally:
            return user
