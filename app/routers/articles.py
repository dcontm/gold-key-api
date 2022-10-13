from fastapi import APIRouter, status, Body, Depends, HTTPException
from typing import List,Any
from sqlalchemy.orm import Session
from fastapi import Body
import models
from schemas import articles, users
from db import get_db
from auth import get_superuser


router = APIRouter()

@router.get('/', response_model=List[articles.Article])
def get_articles(skip:int=0,
            limit:int=100,
            admin:users.User= Depends(get_superuser),
            db: Session = Depends(get_db)
            ):
    articles = db.query(models.Article).offset(skip).limit(limit).all()
    return articles


@router.post('/', response_model=articles.Article)
def create_article(article:articles.ArticleCreate,
                admin:users.User= Depends(get_superuser),
                db: Session = Depends(get_db)
                ):
    db_article = db.query(models.Article).filter(models.Article.title == article.title).first()
    if db_article:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Статья с таким названием уже существует.")
    new_article = models.Article(title=article.title, description=article.description)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

@router.get("/{article_id}", response_model=articles.Article)
def get_article_by_id(article_id:int,
                admin:users.User= Depends(get_superuser),
                db:Session = Depends(get_db)
                ):
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if db_article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Статья с данным id не найдена.")
    return db_article


@router.put("/{article_id}",response_model=articles.Article)
def update_article(article_id:int, 
            article:articles.ArticleUpdate, 
            admin:users.User= Depends(get_superuser),
            db: Session = Depends(get_db)
            ):
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Статья с данным id не найдена.")
    for key,value in article.dict().items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article

@router.delete("/{article_id}")
def delete_article(article_id:int,
            db:Session = Depends(get_db),
            admin:users.User= Depends(get_superuser)
            ):
    db.query(models.Article).filter(models.Article.id == article_id).delete()
    db.commit()
    return f'Статья c id={article_id} успешно удалена.'

