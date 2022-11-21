from fastapi import FastAPI
from .routers import users
from .auth import auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)

@app.route('/')
def index():
    return {"message": "Hello, World"}