import os
from fastapi import APIRouter, status, Body
from aiohttp import ClientSession
from dotenv import load_dotenv
from schemas import notifications

load_dotenv()


router = APIRouter()


@router.post("/")
async def send_norify(notify: notifications.Notify):
    async with ClientSession() as session:
        async with session.post(os.getenv("TELEGRAM_SEND_MESSAGE_URI"),
                                data = {"chat_id": os.getenv("TELEGRAM_CHAT_ID") ,
                                        "parse_mode":"html",
                                        "text":f"<u>{notify.dt}</u>\nИсточник - <b>{notify.target}</b>\n<u>{notify.phone}</u>\n<b>{notify.name}</b>"}) as res:
            result = await res.json()
        return notify

@router.post("/upd", status_code=status.HTTP_200_OK)
async def send_norify():
    async with ClientSession() as session:
        async with session.post(os.getenv("TELEGRAM_GET_UPDATES"))as res:
            result = await res.json()
        return result