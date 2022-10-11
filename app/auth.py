from typing import Union
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import os

from db import get_db
from models import User
from schemas import users, auth_token


load_dotenv()


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def verify_temp_passwod(plain_password, temp_password):
    if plain_password == temp_password:
        return True


def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_by_username(username:str, db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Пользователь с данным номером телефона не найден")
    return db_user

def authenticate_user(username: str, password: str, db:Session = Depends(get_db)):
    user = get_user_by_username(username, db)
    if not user:
        return False
    if not user.hashed_password and verify_temp_passwod(password, user.temp_password):
        return user        
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = auth_token.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user



async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

async def get_superuser(user: User = Depends(get_current_active_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only for superuser")
    return user