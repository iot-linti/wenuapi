from .common import CommonColumns
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Boolean,
    Float,
)


class Measurement(CommonColumns):
    __tablename__ = 'measurement'
    _id = Column(Integer, primary_key=True, autoincrement=True)
    mote_id = Column(Integer)  # , ForeignKey('mote._id'))
    current = Column(Integer)
    movement = Column(Boolean)
    temperature = Column(Float)
    voltage = Column(Integer)
