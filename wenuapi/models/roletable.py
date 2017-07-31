
from .common import CommonColumns
from sqlalchemy.orm import relationship
from .user import User
from .role import Role
from sqlalchemy import (
    Column,
    String,
    UniqueConstraint,
    DateTime,
    ForeignKey,
    Integer,
)

class RoleTable(CommonColumns):
    __tablename__ = 'roletable'
    #__table_args__ = (UniqueConstraint('user_id', 'role_id', name='my_2uniq'),) #No funciona en Eve

    _id = Column(Integer, primary_key=True, autoincrement=True)
    user_id =  Column(Integer, ForeignKey('user._id'))
    role_id = Column(Integer, ForeignKey('role._id'))
    users = relationship(User, uselist=False)
    roles = relationship(Role, uselist=False)

