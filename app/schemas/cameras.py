from pydantic import BaseModel

class Camera(BaseModel):
    id: int
    title: str
    description: str
