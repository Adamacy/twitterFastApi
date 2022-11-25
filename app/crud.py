from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.db import get_db
import app.models as models
import app.schema as schema

from .auth import auth

def get_user_by_username(db: Session, username: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()

    return db_user

    
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

    tweet = models.Tweet(description = tweet.description, likes = 0, author_id = author_id)

    db.add(tweet)
    db.commit()
    db.refresh(tweet)

    return tweet

def update_tweet(db: Session, tweet_id: int, element: str, data: str | None = None):
    db_tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
    if db_tweet is None:
        return HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Tweet not found")
    
    if element == 'likes':
        db_tweet.likes += 1

    if element == 'description':

        db_tweet.description = data
    
    db.commit()
    db.refresh(db_tweet)
