from typing import Any
from fastapi import APIRouter
import vk

router = APIRouter()

@router.get('/', response_model=Any)
def get_news_from_vk(skip:int=0, limit:int=10):
    posts = vk.api.wall.get(owner_id="-43822083", count=limit, offset=skip)
    return posts