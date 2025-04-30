from sqlalchemy import Column 
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.session import Base

from datetime import datetime
class MahasiswaDosen(Base):
    __tablename__ = "mahasiswa_dosen"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mahasiswa_nim = Column(String, ForeignKey("mahasiswa.nim", ondelete="CASCADE"), nullable=False)
    dosen_alias = Column(String, ForeignKey("dosen.alias", ondelete="CASCADE"), nullable=False)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    
    mahasiswa = relationship("Mahasiswa", back_populates="dosen_relation")
    dosen = relationship("Dosen", back_populates="mahasiswa_relation")
    
    __table_args__ = (
        UniqueConstraint("mahasiswa_nim", "dosen_alias", "role", name="unique_mahasiswa_dosen_role"),
    )