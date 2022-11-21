from fastapi import APIRouter, Depends, status, HTTPException
from ..schema import User, UserCreate
from sqlalchemy.orm import Session
from ..crud import get_user_by_username, create_user
from ..db import get_db

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post("/create")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db = db, username = user.username)
    if db_user:
        return HTTPException(status.HTTP_403_FORBIDDEN, detail="User already exist")
    create_user(db = db, user = user)
    return HTTPException(status_code = status.HTTP_201_CREATED, detail="User has beed created")