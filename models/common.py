from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
)
from sqlalchemy_utils import PasswordType
Base = declarative_base()


class CommonColumns(Base):
    __abstract__ = True
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))


class User(CommonColumns):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
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
