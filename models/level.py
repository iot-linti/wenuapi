from .common import CommonColumns
from .mote import Mote
from sqlalchemy import (
    Column,
    String,
    Integer,
)
from sqlalchemy.orm import relationship


class Level(CommonColumns):
    __tablename__ = 'level'
    _id = Column(Integer, primary_key=True, autoincrement=True)
    map = Column(String(160))
