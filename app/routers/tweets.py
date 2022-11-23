from fastapi import APIRouter, Depends, status, Response, Cookie
from fastapi.responses import RedirectResponse
from ..db import get_db
from ..crud import get_tweets, create_tweet, update_tweet
from ..schema import TweetCreate, User, TweetUpdate
from ..auth.auth import get_current_active_user
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/tweets",
    tags=['tweets']
)

@router.get("/")
def take_all_tweets(db: Session = Depends(get_db)):
    return get_tweets(db = db)

@router.post('/')
async def create_tweet_route(tweet: TweetCreate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return create_tweet(db = db, tweet = tweet, author_id = current_user.id)

@router.post('/{tweet_id}/{element}/update')
def update_likes(tweet_id: int, element: str, data: TweetUpdate, db: Session = Depends(get_db)):
    return update_tweet(db = db, tweet_id = tweet_id, element = element, data = data.description)