from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class MahasiswaSchema(BaseModel):
    id: UUID
    nim: str
    nama: str
    email: str
    # password: str
    topik_penelitian: Optional[str] = None
    avatar_url: Optional[str] = None  
    semester_saat_ini: Optional[int] = None  
    status_mahasiswa: Optional[str] = "Aktif"

    class Config:
        from_attributes = True

class MahasiswaUpdateSchema(BaseModel):
    nama: Optional[str] = None
    email: Optional[str] = None
    # password: Optional[str] = None
    topik_penelitian: Optional[str] = None
    avatar_url: Optional[str] = None  
    semester_saat_ini: Optional[int] = None  
    status_mahasiswa: Optional[str] = None

class MahasiswaCreateSchema(BaseModel):
    nim: str
    nama: str
    email: str
    password: str

class MahasiswaResponseSchema(BaseModel):
    nim: str
    nama: str
    email: str
    # password: str
    topik_penelitian: Optional[str] = None
    avatar_url: Optional[str] = None  
    semester_saat_ini: Optional[int] = None  
    status_mahasiswa: Optional[str] = None