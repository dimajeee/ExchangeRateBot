from sqlalchemy import Column, Integer, String, BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BIGINT, unique=True, index=True)
    name = Column(String, index=True)
