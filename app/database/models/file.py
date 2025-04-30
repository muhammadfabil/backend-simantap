from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime 
from sqlalchemy import ForeignKey
from sqlalchemy import Integer 
from sqlalchemy import String 
from sqlalchemy import Text

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Relationship
from sqlalchemy.sql import func

from datetime import datetime

from app.database.session import Base

import uuid

class Files(Base):
    __tablename__ = "files"

    file_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    antrian_id = Column(Integer, ForeignKey("antrian_bimbingan.id_antrian", ondelete="CASCADE"), nullable=False)
    mahasiswa_nim = Column(String, ForeignKey("mahasiswa.nim", ondelete="CASCADE"), nullable=False)
    
    filename = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    is_checked = Column(Boolean, nullable=False, default=False)
    keterangan = Column(Text)

    created_at = Column(DateTime, default=func.now())
    update_at = Column(DateTime, onupdate=func.now())

    antrian_bimbingan = Relationship("AntrianBimbingan", back_populates="files") 
    mahasiswa = Relationship("Mahasiswa", back_populates="files")