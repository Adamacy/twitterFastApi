from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class TweetBase(BaseModel):
    description: str
    likes: int | None = None

class TweetCreate(TweetBase):
    pass

class Tweet(TweetBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True

class TweetUpdate(BaseModel):
    description: str | None = None

class UserBase(BaseModel):
    username: str
    fullname: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    tweets: list[Tweet] = []

    class Config:
        orm_mode = True