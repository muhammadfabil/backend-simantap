from sqlalchemy import Boolean
from sqlalchemy import Column 
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database.session import Base

from datetime import datetime

import uuid

class Layanan(Base):
    __tablename__ = "layanan"

    layanan_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    layanan_jenis = Column(String, nullable=False)
    layanan_file = Column(String, unique=True, nullable=False)
    layanan_status = Column(Integer,default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    update_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

class JenisLayanan(Base):
    __tablename__ = "jenis_layanan"

    id = Column(Integer, primary_key=True, index=True)
    nama_layanan = Column(String, nullable=False, unique=True)
    deskripsi = Column(Text)
    is_aktif = Column(Boolean, default=True)
    url_file = Column(String)

    dokumen_persyaratan =  Relationship("DokumenPersyaratan", back_populates="jenis_layanan", cascade="all, delete-orphan")
    pengajuan = Relationship("PengajuanLayanan", back_populates="jenis_layanan", cascade="all, delete-orphan")


class DokumenPersyaratan(Base):
    __tablename__ = "dokumen_persyaratan"

    id = Column(Integer, primary_key=True, index=True)
    jenis_layanan_id = Column(Integer, ForeignKey("jenis_layanan.id", ondelete="CASCADE"), nullable=False)
    nama_dokumen = Column(String, nullable=False)
    is_wajib = Column(Boolean, default=True)

    jenis_layanan = Relationship("JenisLayanan", back_populates="dokumen_persyaratan")


class PengajuanLayanan(Base):
    __tablename__ = "pengajuan_layanan"

    # id = Column(Integer, primary_key=True, index=True)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    mahasiswa_nim = Column(String, ForeignKey("mahasiswa.nim", ondelete="CASCADE"), nullable=False)
    jenis_layanan_id = Column(Integer, ForeignKey("jenis_layanan.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, default="Menunggu")
    catatan_admin = Column(Text, nullable=True)
    jadwal_pengambilan = Column(DateTime, nullable=True)
    timestamp_diproses = Column(DateTime, nullable=True)
    timestamp_selesai = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now())

    jenis_layanan = Relationship("JenisLayanan", back_populates="pengajuan")
    lampiran = Relationship("LampiranPengajuan", back_populates="pengajuan", cascade="all, delete-orphan")


class LampiranPengajuan(Base):
    __tablename__ = "lampiran_pengajuan"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    pengajuan_id = Column(UUID(as_uuid=True), ForeignKey("pengajuan_layanan.id", ondelete="CASCADE"), nullable=False)
    nama_dokumen = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.now())

    pengajuan = Relationship("PengajuanLayanan", back_populates="lampiran")