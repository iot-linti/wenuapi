from .common import CommonColumns
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Boolean,
)


class Action(CommonColumns):
    __tablename__ = 'action'
    id = Column(Integer, primary_key=True, autoincrement=True)
    mote_id = Column(Integer)  # , ForeignKey('mote._id'))
    level_id = Column(Integer)  # , ForeignKey('level._id'))
    turn_off = Column(Boolean)
