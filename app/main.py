from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from routers import notify

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
    notify.router,
    prefix="/notify",
    tags=["notify"],
)
