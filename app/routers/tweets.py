from fastapi import APIRouter, Depends, status, Response, Cookie
from fastapi.responses import RedirectResponse
from ..db import get_db
from ..crud import get_tweets, create_tweet
from ..schema import TweetCreate, User
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
    print(current_user.id)
    return create_tweet(db = db, tweet = tweet, author_id = current_user.id)