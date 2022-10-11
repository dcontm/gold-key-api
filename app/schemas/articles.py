from datetime import datetime
from pydantic import BaseModel

class BaseArticle(BaseModel):
    title: str
    description: str = None
    content: str = None


class ArticleCreate(BaseArticle):
    pass

class ArticleUpdate(BaseArticle):
    published: bool

class Article(BaseArticle):
    id: str
    created: datetime

    class Config:
        orm_mode = True
