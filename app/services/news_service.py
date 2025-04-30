from fastapi import HTTPException
from fastapi import UploadFile
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.database.models.news import News
from app.schemas.news import NewsCreate, NewsUpdate
from app.middleware.supabase_client import SupabaseClient

supabase = SupabaseClient()

def create_news(db: Session, news_data: NewsCreate, picture: Optional[UploadFile] = None):
    data_dump = news_data.model_dump()
    if picture:
        picture_url = supabase.upload_to_supabase(picture, folder="news")
        data_dump["picture_url"] = picture_url
    
    new_news = News(**data_dump)
    db.add(new_news)
    db.commit()
    db.refresh(new_news)
    return new_news

def get_all_news(db: Session):
    return db.query(News).all()

def get_news_by_id(db: Session, news_id: UUID):
    return db.query(News).filter(News.news_id == news_id).first()

def update_news(db: Session, news_id: UUID, news_data: NewsUpdate, picture: Optional[UploadFile] = None):    
    news = get_news_by_id(db, news_id)
    if not news:
        return None
    
    data_dump = news_data.model_dump(exclude_unset=True)
    
    if picture:
        picture_url = supabase.upload_to_supabase(picture, folder="news")
        data_dump["picture_url"] = picture_url

    for key, value in data_dump.items():
        if value is not None:
            if isinstance(value, str):
                value = value.strip()
            setattr(news, key, value)

    db.commit()
    db.refresh(news)
    return news

def delete_news(db: Session, news_id: UUID):
    news = get_news_by_id(db, news_id)
    _title = news.title
    if not news:
        raise HTTPException(status_code=404, detail="No news found")
    db.delete(news)
    db.commit()
    return {
        "message": f"News {_title} has been removed"
    }

def search_news(db: Session, query: str):
    return db.query(News).filter(News.title.ilike(f"%{query}%")).all()

def search_news_by_author(db: Session, author_name: str):
    return db.query(News).filter(News.author_name.ilike(f"{author_name}")).all()

def search_news_by_date(db: Session, start_date: str, end_date: str):
    return db.query(News).filter(News.created_at.between(start_date, end_date)).all()