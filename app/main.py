from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from routers import notifications, users, token
from db import create_bd


app = FastAPI()

# need update for production
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    token.router,
    prefix="/token",
    tags=["auth"],
)

app.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

app.include_router(
    notifications.router,
    prefix="/notify",
    tags=["notify"],
)
