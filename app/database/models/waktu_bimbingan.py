from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Time

from sqlalchemy.orm import relationship

from app.database.session import Base

class WaktuBimbingan(Base):
    __tablename__ = "waktu_bimbingan"

    bimbingan_id = Column(String, primary_key=True, index=True)
    dosen_inisial = Column(String, ForeignKey('dosen.alias', ondelete="CASCADE"), nullable=False)

    tanggal = Column(Date, nullable=False)
    waktu_mulai = Column(Time, nullable=False)
    waktu_selesai = Column(Time, nullable=False)

    jumlah_antrian = Column(Integer, nullable=False, default=5)
    is_active = Column(Boolean, nullable=False, default=True)

    lokasi = Column(String, default="Ruang Prodi", nullable=False)
    keterangan = Column(Text, nullable=True)

    dosen = relationship("Dosen", back_populates="waktu_bimbingan")
    antrian_bimbingan = relationship("AntrianBimbingan", back_populates="waktu_bimbingan", cascade="all, delete-orphan", uselist=True)