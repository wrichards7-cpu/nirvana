from app.factory import Base
from sqlalchemy import create_engine, Column, Integer, String

class Api1(Base):
    __tablename__ = "Api1"
    id = Column(Integer, primary_key=True, autoincrement=True)
    memberid = Column(Integer, index=True)
    oop_max = Column(Integer, index=False)
    remaining_oop_max = Column(Integer, index=False)
    copay = Column(Integer, index=False)

class Api2(Base):
    __tablename__ = "Api2"
    id = Column(Integer, primary_key=True, autoincrement=True)
    memberid = Column(Integer, index=True)
    oop_max = Column(Integer, index=False)
    remaining_oop_max = Column(Integer, index=False)
    copay = Column(Integer, index=False)

class Api3(Base):
    __tablename__ = "Api3"
    id = Column(Integer, primary_key=True, autoincrement=True)
    memberid = Column(Integer, index=True)
    oop_max = Column(Integer, index=False)
    remaining_oop_max = Column(Integer, index=False)
    copay = Column(Integer, index=False)