from sqlalchemy.orm import Session
from fastapi import Depends
from app.db import get_db
import app.models as models
import app.schema as schema

from .auth import auth

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schema.UserCreate):
    
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(username = user.username, fullname = user.fullname, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_tweets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tweet).offset(skip).limit(limit).all()

def create_tweet(db: Session, tweet: schema.TweetCreate, author_id: int):

    tweet = models.Tweet(description = tweet.description, author_id = author_id)

    db.add(tweet)
    db.commit()
    db.refresh(tweet)

    return tweet