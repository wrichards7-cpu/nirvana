from app.factory import Base
from sqlalchemy import create_engine, Column, Integer, String

class Members(Base):
    __tablename__ = "Members"
    memberid = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, index=False)