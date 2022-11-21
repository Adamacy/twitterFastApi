from sqlalchemy.types import String, Integer, Text
from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.db import Base

class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key = True, index=True)
    username = Column(String(30), unique=True)
    fullname = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(Text())

    items = relationship("Tweet", back_populates='owner')


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key = True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(500), index=True)
    likes = Column(Integer)
    author_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates='items')