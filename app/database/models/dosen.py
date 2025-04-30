from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.orm import Relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database.session import Base

from datetime import datetime

import uuid

class Dosen(Base):
    __tablename__ = "dosen"

    id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, index=True)

    alias = Column(String, unique=True, nullable=False, primary_key=True)
    nomor_induk = Column(String)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    keterangan = Column(String, default="")
    status_kehadiran = Column(Boolean, default=True, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    update_at = Column(DateTime, onupdate=datetime.now(), nullable=False)

    # user = Relationship("User", back_populates="dosen")
    waktu_bimbingan = Relationship("WaktuBimbingan", back_populates="dosen", cascade="all, delete-orphan")
    antrian_bimbingan = Relationship("AntrianBimbingan", back_populates="dosen", cascade="all, delete-orphan")
    mahasiswa_relation = Relationship('MahasiswaDosen', back_populates="dosen", cascade="all, delete-orphan")