from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String 
from sqlalchemy.orm import Relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database.session import Base

from datetime import datetime
import uuid

class Mahasiswa(Base):
    __tablename__ = "mahasiswa"

    id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, index=True)

    nim = Column(String, primary_key=True)
    nama = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    topik_penelitian = Column(String)

    avatar_url = Column(String)
    semester_saat_ini = Column(Integer)
    status_mahasiswa = Column(String, default="Aktif")

    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    update_at = Column(DateTime, onupdate=datetime.now(), nullable=False)

    antrian_bimbingan = Relationship("AntrianBimbingan", back_populates="mahasiswa", cascade="all, delete-orphan")
    dosen_relation = Relationship("MahasiswaDosen", back_populates="mahasiswa", cascade="all, delete-orphan")
    files = Relationship("Files", back_populates="mahasiswa", cascade="all, delete-orphan")