from pydantic import BaseModel


class BaseCamera(BaseModel):
    title:str
    description: str = None


class Camera(BaseCamera):
    id: int

    class Config:
        orm_mode = True

class CameraCreate(BaseCamera):
    pass


class CameraUpdate(BaseCamera):
    pass
