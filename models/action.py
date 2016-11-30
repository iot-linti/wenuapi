from .common import CommonColumns
from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    String,
)


class Action(CommonColumns):
    __tablename__ = 'action'
    _id = Column(Integer, primary_key=True, autoincrement=True)
    mote_id = Column(Integer)
    command = Column(String)
    arguments = Column(String)
