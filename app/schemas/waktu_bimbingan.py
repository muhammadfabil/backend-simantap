from pydantic import BaseModel
from pydantic import ConfigDict

from typing import Optional
from typing import List

from datetime import date, time

from app.schemas.antrian_bimbingan import AntrianBimbinganSchema

class WaktuBimbinganSchema(BaseModel):
    bimbingan_id: str
    dosen_inisial: str
    jumlah_antrian: int
    is_active: bool = True
    tanggal: date
    waktu_mulai: time
    waktu_selesai: time
    lokasi: str
    keterangan: Optional[str] = None
    antrian_bimbingan: List[AntrianBimbinganSchema] = []

    model_config = ConfigDict(from_attributes=True)

class CreateWaktuBimbinganSchema(BaseModel):
    dosen_inisial: str
    jumlah_antrian: Optional[int] = 5  # default 5
    is_active: Optional[bool] = True
    tanggal: date
    waktu_mulai: time
    waktu_selesai: time
    lokasi: Optional[str] = "Ruang Prodi"
    keterangan: Optional[str] = None

class UpdateWaktuBimbinganSchema(BaseModel):
    jumlah_antrian: Optional[int] = None
    tanggal: Optional[date] = None
    waktu_mulai: Optional[time] = None
    waktu_selesai: Optional[time] = None
    is_active: Optional[bool] = None
    lokasi: Optional[str] = None
    keterangan: Optional[str] = None