from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional
from uuid import UUID

class DosenSchema(BaseModel):
    id: UUID
    nomor_induk: str
    name: str
    alias: str
    email: str
    # password: str
    keterangan: Optional[str] = "Ruangan Prodi"
    status_kehadiran: Optional[bool] = True
    
    model_config = ConfigDict(from_attributes=True)

class DosenUpdateSchema(BaseModel):
    nomor_induk: Optional[str] = None
    name: Optional[str] = None
    alias: Optional[str] = None
    email: Optional[str] = None
    # password: Optional[str] = None
    keterangan: Optional[str] = None
    status_kehadiran: Optional[bool] = None

class DosenCreateSchema(BaseModel):
    nomor_induk: str
    name: str
    alias: str
    email: str
    password: str

class DosenResponseSchema(BaseModel):
    nomor_induk: str
    name: str
    alias: str
    email: str
    # password: str
    keterangan: Optional[str] = "Ruangan Prodi"
    status_kehadiran: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True) 

