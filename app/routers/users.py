from fastapi import APIRouter, status, Body, Depends, HTTPException
from typing import List
from dotenv import load_dotenv
from sqlalchemy.orm import Session

import models
from schemas import users, cameras
from db import get_db
from auth import get_current_active_user, get_superuser, get_password_hash
from utils import gen_password


load_dotenv()


router = APIRouter()

@router.get('/', response_model=List[users.User])
def get_users(skip:int=0,
            limit:int=100,
            admin:users.User= Depends(get_superuser),
            db: Session = Depends(get_db)
            ):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.post('/', response_model=users.User)
def create_user(user:users.UserCreate,
                admin:users.User= Depends(get_superuser),
                db: Session = Depends(get_db)
                ):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Пользователь с таким номером уже зерегистрирован.")
    new_user = models.User(username=user.username, first_name=user.first_name, second_name=user.second_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/me", response_model=users.User)
def read_users_me(current_user: users.User = Depends(get_current_active_user)):
    return current_user

@router.get("/{user_id}", response_model=users.User)
def get_user_by_id(user_id:int,
                admin:users.User= Depends(get_superuser),
                db:Session = Depends(get_db)
                ):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Пользователь с данным id не найден")
    return db_user

@router.put("/{user_id}",response_model=users.User)
def update_user(user_id:int, 
            user:users.UserUpdate, 
            admin:users.User= Depends(get_superuser), 
            db: Session = Depends(get_db)
            ):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Пользователь с данным id не найден")
    for key,value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id:int,
            db:Session = Depends(get_db),
            admin:users.User= Depends(get_superuser)
            ):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return f'Пользователь c id={user_id} успешно удален.'

@router.post("/{user_id}/bind_camera",response_model=users.User)
def update_user(user_id:int, 
            camera_id: int = Body(...),
            admin:users.User= Depends(get_superuser), 
            db: Session = Depends(get_db)
            ):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Пользователь с данным id не найден")

    camera = db.query(models.Camera).filter(models.Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Нет камеры с id={camera_id}.")
    db_user.camera.append(camera)
    db.commit()
    return db_user

@router.post("/{user_id}/unbind_camera",response_model=users.User)
def update_user(user_id:int, 
            camera_id: int = Body(...),
            admin:users.User= Depends(get_superuser), 
            db: Session = Depends(get_db)
            ):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Пользователь с данным id не найден")

    camera = db.query(models.Camera).filter(models.Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Нет камеры с id={camera_id}.")
    db_user.camera.remove(camera)
    db.commit()
    return db_user


@router.post('/set_password')
def set_password(password:str=Body(...),
                db:Session = Depends(get_db),
                current_user: users.User = Depends(get_current_active_user),
                ):
    hashed_password = get_password_hash(password)
    current_user.hashed_password = hashed_password
    current_user.const_password = True
    db.commit()
    return 'Новый пароль успешно установлен.'

@router.post('/reset_password')
def reset_password(db:Session = Depends(get_db),
                current_user: users.User = Depends(get_current_active_user),
                ):
    current_user.hashed_password = None
    current_user.temp_password = gen_password()
    db.commit()
    return 'Пароль успешно сброшен. Новый временный пароль вы сможете получить у администратора.'



