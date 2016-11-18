from .common import CommonColumns
from sqlalchemy import (
    Column,
    Integer,
    Boolean,
)


class Action(CommonColumns):
    __tablename__ = 'action'
    id = Column(Integer, primary_key=True, autoincrement=True)
    mote_id = Column(Integer)
    level_id = Column(Integer)
    turn_off = Column(Boolean)
