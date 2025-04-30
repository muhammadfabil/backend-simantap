from pydantic import BaseModel
from pydantic import ConfigDict

from typing import Optional

from uuid import UUID

from datetime import datetime

class FileCreateSchema(BaseModel):
    antrian_id: int
    mahasiswa_nim: str
    filename: str
    file_url: str
    is_checked: Optional[bool] = False
    keterangan: Optional[str] = None

class FileUpdateSchema(BaseModel):
    filename: Optional[str] = None
    file_url: Optional[str] = None
    is_checked: Optional[bool] = None
    keterangan: Optional[str] = None

class FileSchema(BaseModel):
    file_id: UUID
    antrian_id: UUID
    mahasiswa_nim: str
    filename: str
    file_url: str
    is_checked: bool
    keterangan: Optional[str] = None
    created_at: datetime
    update_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
