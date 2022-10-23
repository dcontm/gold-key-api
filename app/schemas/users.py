from typing import Any, List, Union
from pydantic import BaseModel
from . cameras import Camera


class UserBase(BaseModel):
    username: str
    first_name: str
    second_name: str


class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    temp_password: str
    camera: List[Camera] = []
    const_password: bool

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    is_active: bool
    is_superuser: bool
    temp_password: str
