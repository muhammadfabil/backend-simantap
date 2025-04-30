from fastapi import APIRouter, Depends, HTTPException
from fastapi import File
from fastapi import Form
from fastapi import UploadFile
from sqlalchemy.orm import Session
from typing import Optional

from app.services.news_service import *
from app.schemas.news import NewsCreate, NewsUpdate, NewsResponse

from app.database.session import get_db

from uuid import UUID

router = APIRouter(prefix="/news", tags=["News"])

@router.post("/", response_model=NewsResponse)
def create_news_route(
    author_name: Optional[str] = Form("Admin"),
    author_email: Optional[str] = Form(None),
    picture_description: Optional[str] = Form(None),
    title: str = Form(...),
    subtitle: Optional[str] = Form(None),
    content: str = Form(...),
    status: Optional[str] = Form("draft"),
    picture: Optional[UploadFile] = File(None), 
    db: Session = Depends(get_db)
):
    news_data = NewsCreate(
        author_name=author_name,
        author_email=author_email,
        picture_description=picture_description,
        title=title,
        subtitle=subtitle,
        content=content,
        status=status
    )

    return create_news(db, news_data, picture)

@router.get("/", response_model=list[NewsResponse])
def get_news_route(db: Session = Depends(get_db)):
    news_list = get_all_news(db)
    if not news_list:
        raise HTTPException(status_code=404, detail="No news found")
    return news_list

@router.get("/{news_id}", response_model=NewsResponse)
def get_news_by_id_route(news_id: UUID, db: Session = Depends(get_db)):
    news = get_news_by_id(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news

@router.put("/{news_id}", response_model=NewsResponse)
def update_news_route(
    news_id: UUID,
    author_name: Optional[str] = Form(None),
    author_email: Optional[str] = Form(None),
    picture_description: Optional[str] = Form(None),
    title: Optional[str] = Form(None),
    subtitle: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    status: Optional[str] = Form(None),
    picture: Optional[UploadFile] = File(None), 
    db: Session = Depends(get_db)
):
    news_data = NewsUpdate(
        author_name=author_name,
        author_email=author_email,
        picture_description=picture_description,
        title=title,
        subtitle=subtitle,
        content=content,
        status=status
    )
    updated_news = update_news(db, news_id, news_data, picture)
    if not updated_news:
        raise HTTPException(status_code=404, detail="News not found")
    return updated_news

@router.delete("/{news_id}")
def delete_news_route(news_id: UUID, db: Session = Depends(get_db)):
    news = delete_news(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news

@router.get("/search", response_model=list[NewsResponse])
def search_news_route(query: str, db: Session = Depends(get_db)):
    search_results = search_news(db, query)
    if not search_results:
        raise HTTPException(status_code=404, detail="No news found")
    return search_results

@router.get("/search/author", response_model=list[NewsResponse])
def search_news_by_author_route(author_name: str, db: Session = Depends(get_db)):
    search_results = search_news_by_author(db, author_name)
    if not search_results:
        raise HTTPException(status_code=404, detail="No news found")
    return search_results

@router.get("/search/date", response_model=list[NewsResponse])
def search_news_by_date_route(start_date: str, end_date: str, db: Session = Depends(get_db)):
    search_result = search_news_by_date(db, start_date, end_date)
    if not search_result:
        raise HTTPException(status_code=404, detail="No news found")
    return search_result
