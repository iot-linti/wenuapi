from .common import CommonColumns
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
)


class Alert(CommonColumns):
    __tablename__ = 'alert'
    _id = Column(Integer, primary_key=True, autoincrement=True)
    mote_id = Column(Integer, ForeignKey('mote._id'))
    measurement_id = Column(Integer, ForeignKey('measurement._id'))
    time = Column(DateTime)
    solved = Column(Boolean)
