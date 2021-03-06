from .common import CommonColumns
from sqlalchemy import (
    Column,
    String,
    Integer,
)


class Mote(CommonColumns):
    __tablename__ = 'mote'
    _id = Column(Integer, primary_key=True, autoincrement=True)
    level_id = Column(Integer, nullable=False)
    mote_id = Column(String(80), nullable=False)
    resolution = Column(String(80), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
