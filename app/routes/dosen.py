from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.services.dosen_service import *
from app.services.bimbingan_service import *

from app.schemas.dosen import *

from app.middleware.security import require_roles

router = APIRouter(prefix="/dosen", tags=["Dosen"])

@router.post("/", response_model=DosenSchema, dependencies=[Depends(require_roles("admin"))])
def create_dosen_route(dosen: DosenCreateSchema, db: Session = Depends(get_db)):
    return create_dosen(db, dosen)

@router.get("/all", response_model=list[DosenSchema])
def get_all_dosen_route(db: Session = Depends(get_db)):
    return get_all_dosen(db)

@router.get("/{inisial}", response_model=DosenSchema)
def get_dosen_route(inisial: str, db: Session = Depends(get_db)):
    
    data = get_dosen(db, inisial)
    if not data:
        raise HTTPException(status_code=404, detail="Data not Found")
    
    waktu_bimbingan = get_waktu_bimbingan_from_dosen(db, inisial)
    
    return JSONResponse (content={
        "dosen": {
            "nomor_induk": data.nomor_induk,
            "name": data.name,
            "alias": data.alias,
            "email": data.email,
            "status_kehadiran": data.status_kehadiran,
            "keterangan": data.keterangan
        },
        "waktu_bimbingan": [
            {
                "bimbingan_id": item.bimbingan_id,
                "tanggal": str(item.tanggal),
                "waktu_mulai": str(item.waktu_mulai),
                "waktu_selesai": str(item.waktu_selesai),
                "lokasi": item.lokasi,
                "keterangan": item.keterangan
            }
            for item in waktu_bimbingan
        ]
    })

@router.put("/{inisial}")
async def update_dosen_route(inisial: str, dosen_data: DosenUpdateSchema, db: Session = Depends(get_db)):
    dosen = update_dosen(db, inisial, dosen_data)
    if not dosen:
        raise HTTPException(status_code = 404, detail = "Dosen Tidak Ditemukan")
    return {"Message": "Dosen Telah diUpdate", "data":dosen}

@router.get("/admin/{dosen_id}")
def get_dosen_detail_route(dosen_id: UUID, db: Session = Depends(get_db)):
    return get_detail_dosen(db, dosen_id)

@router.delete("/{dosen_id}", dependencies=[Depends(require_roles("admin"))])
def delete_dosen_route(dosen_id: UUID, db: Session = Depends(get_db)):
    return delete_dosen(db, dosen_id)