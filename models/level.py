from .common import CommonColumns
from sqlalchemy import (
    Column,
    String,
    Integer,
)


class Level(CommonColumns):
    __tablename__ = 'level'
    _id = Column(Integer, primary_key=True, autoincrement=True)
    map = Column(String(160))
