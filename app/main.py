from fastapi import FastAPI
from .routers import users, tweets
from .auth import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tweets.router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials = True,
    allow_origins=[
        'http://localhost:8080',
        'http://localhost:8000/'
    ],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type","Set-Cookie"],
    
)
