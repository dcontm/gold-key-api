import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Table, DateTime
from sqlalchemy.orm import relationship

from db import Base
from utils import gen_password



association_table = Table(
    "association",
    Base.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("camera_id", ForeignKey("camera.id")),
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    second_name = Column(String)
    hashed_password = Column(String, nullable=True)
    temp_password = Column(String, default=gen_password)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    camera = relationship("Camera", secondary=association_table)


class Camera(Base):
    __tablename__ = "camera"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=False, default='')


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=False, default='')
    content = Column(Text, nullable=False, default='')
    created = Column(DateTime, default=datetime.datetime.utcnow)

