from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, status, Response
from fastapi.exceptions import HTTPException
from app.db import get_db
from app.schema import TokenData, User
import os
from sqlalchemy.orm import Session
import app.crud as crud
from datetime import timedelta, datetime
from jose import JWTError, jwt
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi import APIRouter
from app import schema
from uuid import uuid4, UUID

router = APIRouter(
    prefix = '/v1',
    tags = ["auth"]
)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def verify_password(password, hashed_password):

    return pwd_context.verify(password, hashed_password)


def hash_password(password):

    return pwd_context.hash(password)


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):

    user = crud.get_user_by_username(db = db, username = username)
    if not user:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(password, user.password):
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="Password incorrect")

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime().utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"
    })

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_username(username = username, db = db)
    if user is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    
    return current_user


@router.post('/token', response_model=schema.Token)
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db = db, username = form_data.username, password = form_data.password)
    print(user)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(data = {"sub": user.username}, expires_delta = access_token_expires)

    session = uuid4()

    response.set_cookie("token", access_token, expires=14 * 24 * 60 * 60, httponly=True, secure=True, samesite='none')

    return {"access_token": access_token, "token_type": "bearer"}
