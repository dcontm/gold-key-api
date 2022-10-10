from typing import List, Union
from pydantic import BaseModel
from . cameras import Camera


class UserBase(BaseModel):
    username: str
    first_name: str
    second_name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    temp_password: str
    camera: List[Camera] = []

    class Config:
        orm_mode = True

class UserUpdate(UserBase):
    is_active: bool
    temp_password: str
    camera: List[Camera] = []

class UserSetPassword(User):
    password: str
