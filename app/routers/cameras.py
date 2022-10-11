from fastapi import APIRouter, status, Body, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

import models
from schemas import cameras, users
from db import get_db
from auth import get_superuser


router = APIRouter()

@router.get('/', response_model=List[cameras.Camera])
def get_cameras(skip:int=0,
            limit:int=100,
            admin:users.User= Depends(get_superuser),
            db: Session = Depends(get_db)
            ):
    cameras = db.query(models.Camera).offset(skip).limit(limit).all()
    return cameras

@router.post('/', response_model=cameras.Camera)
def create_camera(camera:cameras.CameraCreate,
                admin:users.User= Depends(get_superuser),
                db: Session = Depends(get_db)
                ):
    db_camera = db.query(models.Camera).filter(models.Camera.title == camera.title).first()
    if db_camera:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Камера с таким названием уже существует.")
    new_camera = models.Camera(title=camera.title, description=camera.description)
    db.add(new_camera)
    db.commit()
    db.refresh(new_camera)
    new_camera = db.query(models.Camera).filter(models.Camera.title == camera.title).first()
    return new_camera

@router.get("/{camera_id}", response_model=cameras.Camera)
def get_camera_by_id(camera_id:int,
                admin:users.User= Depends(get_superuser),
                db:Session = Depends(get_db)
                ):
    db_camera = db.query(models.Camera).filter(models.Camera.id == camera_id).first()
    if db_camera is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Камера с данным id не найдена.")
    return db_camera

@router.put("/{camera_id}",response_model=cameras.Camera)
def update_camera(camera_id:int, 
            camera:cameras.CameraUpdate, 
            admin:users.User= Depends(get_superuser), 
            db: Session = Depends(get_db)
            ):
    db_camera = db.query(models.Camera).filter(models.Camera.id == camera_id).first()
    if not db_camera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Камера с данным id не найдена.")
    for key,value in camera.dict().items():
        setattr(db_camera, key, value)
    db.commit()
    db.refresh(db_camera)
    return db_camera

@router.delete("/{camera_id}")
def delete_camera(camera_id:int,
            db:Session = Depends(get_db),
            admin:users.User= Depends(get_superuser)
            ):
    db.query(models.Camera).filter(models.Camera.id == camera_id).delete()
    db.commit()
    return f'Камера c id={camera_id} успешно удалена.'

