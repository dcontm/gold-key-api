from typing import Any
from pydantic import BaseModel
import pendulum

class Notify(BaseModel):
    dt: Any = pendulum.now(tz='Europe/Moscow').to_datetime_string()
    target: str
    name: str
    phone: str

    class Config:
        orm_mode = True
