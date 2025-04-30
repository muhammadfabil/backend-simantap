from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.bimbingan_service import *
from app.schemas.waktu_bimbingan import *

from app.database.session import get_db

router = APIRouter(prefix="/waktu_bimbingan", tags=["Waktu Bimbingan"])

@router.post("/", response_model=WaktuBimbinganSchema)
async def create_waktu_bimbingan_route(waktu_bimbingan: CreateWaktuBimbinganSchema, db: Session = Depends(get_db)):
    return await create_waktu_bimbingan(db, waktu_bimbingan)

@router.get("/{bimbingan_id}", response_model=WaktuBimbinganSchema)
def get_waktu_bimbingan_route(bimbingan_id: str, db: Session = Depends(get_db)):
    return get_waktu_bimbingan(db, bimbingan_id)

@router.get("/dosen/{dosen_inisial}", response_model=List[WaktuBimbinganSchema])
def get_bimbingan_by_dosen(dosen_inisial: str, db: Session = Depends(get_db)):
    return get_waktu_bimbingan_from_dosen(db, dosen_inisial)

@router.put("/{bimbingan_id}", response_model=WaktuBimbinganSchema)
async def update_waktu_bimbingan_route(bimbingan_id: str, updated_data: UpdateWaktuBimbinganSchema, db: Session = Depends(get_db)):
    return await update_waktu_bimbingan(db, bimbingan_id, updated_data)

@router.delete("/{bimbingan_id}")
def delete_waktu_bimbingan_route(bimbingan_id: str, db: Session = Depends(get_db)):
    return delete_waktu_bimbingan(db, bimbingan_id)

