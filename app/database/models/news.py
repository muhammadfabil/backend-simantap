from sqlalchemy import Column
from sqlalchemy import DateTime 
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database.session import Base

from datetime import datetime
import uuid

class News(Base):
    __tablename__ = "news"

    news_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    author_name = Column(String(255), nullable=False, default="Admin")
    author_email = Column(String(255), nullable=True)
    picture_url = Column(String(500), nullable=True)
    picture_description = Column(String(255), nullable=True)
    title = Column(String(255), nullable=False)
    subtitle = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="draft")
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    update_at = Column(DateTime, onupdate=datetime.now)
