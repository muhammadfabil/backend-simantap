from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from typing import Optional

from uuid import UUID

from datetime import datetime

class NewsCreate(BaseModel):
    author_name: Optional[str] = Field(default="Admin", max_length=255) 
    author_email: Optional[str] = Field(default=None, max_length=255)
    picture_url: Optional[str] = Field(default=None, max_length=500)
    picture_description: Optional[str] = Field(default=None, max_length=255)
    title: str = Field(..., max_length=255)
    subtitle: Optional[str] = Field(default=None, max_length=255)
    content: str
    status: Optional[str] = Field(default="draft", max_length=50)

    model_config=ConfigDict(from_attributes=True)

class NewsUpdate(BaseModel):
    author_name: Optional[str] = Field(default=None, max_length=255) 
    author_email: Optional[str] = Field(default=None, max_length=255)
    picture_url: Optional[str] = Field(default=None, max_length=500)
    picture_description: Optional[str] = Field(default=None, max_length=255)
    title: Optional[str] = Field(default=None, max_length=255)
    subtitle: Optional[str] = Field(default=None, max_length=255)
    content: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None, max_length=50)

    model_config=ConfigDict(from_attributes=True)

class NewsResponse(BaseModel):
    news_id: UUID
    author_name: str 
    author_email: Optional[str]
    picture_url: Optional[str] 
    picture_description: Optional[str] 
    title: str 
    subtitle: Optional[str]
    content: str
    status: str
    created_at: datetime
    update_at: Optional[datetime]

    model_config=ConfigDict(from_attributes=True)