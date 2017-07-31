from .common import CommonColumns
from sqlalchemy.orm.exc import NoResultFound
from flask import current_app as app
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
)

class Role(CommonColumns):
    __tablename__ = 'role'
    _id = Column(Integer, primary_key=True, autoincrement=True)
    rolename = Column(String(80),unique=True)

    @classmethod
    def set_Role(cls, rolename, session=None):
        if session is None:
            session = app.data.driver.session

        try:
            role = session.query(Role).filter(Role.rolename == rolename).one()
        except NoResultFound:
            role = Role(rolename = rolename)
            session.add(role)
            session.commit()

        return role
