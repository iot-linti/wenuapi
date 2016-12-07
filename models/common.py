from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy import (
    Column,
    DateTime,
    String,
)
Base = declarative_base()


class CommonColumns(Base):
    __abstract__ = True
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))
