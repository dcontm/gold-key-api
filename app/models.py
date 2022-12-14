import datetime
from email.policy import default
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Table, DateTime
from sqlalchemy.orm import relationship

from db import Base
from utils import gen_password



association_table = Table(
    "association",
    Base.metadata,
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE")),
    Column("camera_id", ForeignKey("camera.id", ondelete="CASCADE")),
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
    const_password = Column(Boolean, default=False)
    camera = relationship("Camera", secondary=association_table, back_populates="users", cascade="all, delete")


class Camera(Base):
    __tablename__ = "camera"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=False, default='')
    users = relationship("User", secondary=association_table, back_populates="camera", passive_deletes=True)


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=False, default='')
    content = Column(Text, nullable=False, default='')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    is_published = Column(Boolean, default=False)

