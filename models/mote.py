from .common import CommonColumns
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
)


class Mote(CommonColumns):
    __tablename__ = 'mote'
    _id = Column(Integer, primary_key=True, autoincrement=True)
    level_id = Column(Integer) # , ForeignKey('level.id'))
    mote_id = Column(String(80))
    resolution = Column(String(80))
    x = Column(Integer)
    y = Column(Integer)
