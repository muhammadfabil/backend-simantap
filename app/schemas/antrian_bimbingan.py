from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.schemas.file import FileSchema  

class AntrianBimbinganSchema(BaseModel):
    id_antrian: UUID
    mahasiswa_nim: str
    waktu_id: str
    dosen_inisial: str
    status_antrian: str = "Menunggu"
    position: int
    created_at: datetime
    files: Optional[FileSchema] = None

    class Config:
        from_attributes = True

class AmbilAntrianSchema(BaseModel):
    mahasiswa_nim: str
    waktu_id: str

class AmbilAntrianResponse(BaseModel):
    message: str
    posisi: int
    id_antrian: UUID
    antrian: AmbilAntrianSchema
    files: Optional[FileSchema] = None

class AntrianBimbinganResponse(BaseModel):
    id_antrian: UUID
    mahasiswa_nim: str
    dosen_inisial: str
    waktu_id: str
    status_antrian: str = "Menunggu"
    position: int
    created_at: datetime
    files: Optional[FileSchema] = None

class UpdateAntrianSchema(BaseModel):
    status_antrian: Optional[str] = None
    position: Optional[int] = None
