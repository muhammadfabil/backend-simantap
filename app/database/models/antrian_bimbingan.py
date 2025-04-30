from sqlalchemy import Column 
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey 
from sqlalchemy import Integer
from sqlalchemy import String 
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database.session import Base

from datetime import datetime

import uuid

class AntrianBimbingan(Base):
    __tablename__ = "antrian_bimbingan"

    id_antrian = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid.uuid4)
    mahasiswa_nim = Column(String, ForeignKey("mahasiswa.nim", ondelete="CASCADE"), nullable=False)
    waktu_id = Column(String, ForeignKey("waktu_bimbingan.bimbingan_id", ondelete="CASCADE"), nullable=False)
    dosen_inisial = Column(String, ForeignKey("dosen.alias", ondelete="CASCADE"), nullable=False)
    
    status_antrian = Column(String, nullable=False, default="Menunggu")
    position = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    
    dosen = relationship("Dosen", back_populates="antrian_bimbingan")
    files = relationship("Files", back_populates="antrian_bimbingan", cascade="all, delete-orphan", uselist=False) 
    mahasiswa = relationship("Mahasiswa", back_populates="antrian_bimbingan")
    waktu_bimbingan = relationship("WaktuBimbingan", back_populates="antrian_bimbingan")
