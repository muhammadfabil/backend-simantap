from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.models.waktu_bimbingan import WaktuBimbingan
from app.routes.websocket_router import manager
from app.schemas.waktu_bimbingan import *


async def create_waktu_bimbingan(db: Session, waktu_bimbingan_schema: CreateWaktuBimbinganSchema):
    
    db_waktu_bimbingan = WaktuBimbingan(
        dosen_inisial=waktu_bimbingan_schema.dosen_inisial,
        jumlah_antrian=waktu_bimbingan_schema.jumlah_antrian,
        tanggal=waktu_bimbingan_schema.tanggal,
        is_active=waktu_bimbingan_schema.is_active,
        waktu_mulai=waktu_bimbingan_schema.waktu_mulai,
        waktu_selesai=waktu_bimbingan_schema.waktu_selesai,
        lokasi=waktu_bimbingan_schema.lokasi,
        keterangan=waktu_bimbingan_schema.keterangan
    )
    
    existing_count = db.query(WaktuBimbingan).filter(WaktuBimbingan.dosen_inisial == waktu_bimbingan_schema.dosen_inisial).count()
    db_waktu_bimbingan.bimbingan_id = f"{waktu_bimbingan_schema.dosen_inisial.upper()}{existing_count + 1}" 
    
    payload = {
        "event": "create_waktu_bimbingan",
        "inisial": waktu_bimbingan_schema.dosen_inisial,
        "waktu_id": db_waktu_bimbingan.bimbingan_id,
        "tanggal": str(waktu_bimbingan_schema.tanggal),
        "waktu_mulai": str(waktu_bimbingan_schema.waktu_mulai),
        "waktu_selesai": str(waktu_bimbingan_schema.waktu_selesai),
        "jumlah_antrian": waktu_bimbingan_schema.jumlah_antrian,
        "lokasi": waktu_bimbingan_schema.lokasi,
        "keterangan": waktu_bimbingan_schema.keterangan
    }

    from app.services.relasi_service import get_relation_by_dosen
    relasi_list = get_relation_by_dosen(db, waktu_bimbingan_schema.dosen_inisial)
    mahasiswa_nim_list = [relasi.mahasiswa_nim for relasi in relasi_list]

    for nim in mahasiswa_nim_list:
        await manager.send_json(
            user_id=nim,
            data=payload
        )

    # await manager.broadcast_all(
    #     message=payload
    # )
    
    db.add(db_waktu_bimbingan)
    db.commit()
    db.refresh(db_waktu_bimbingan)
    return db_waktu_bimbingan

def get_waktu_bimbingan(db: Session, bimbingan_id: str):
    waktu = db.query(WaktuBimbingan).filter(WaktuBimbingan.bimbingan_id == bimbingan_id).first()
    if not waktu:
        raise HTTPException(status_code=404, detail="Waktu bimbingan tidak ditemukan")
    return WaktuBimbinganSchema.model_validate(waktu)


def get_waktu_bimbingan_from_dosen(db: Session, dosen_inisial: str):
    waktu_list = db.query(WaktuBimbingan).filter(WaktuBimbingan.dosen_inisial == dosen_inisial).order_by(WaktuBimbingan.bimbingan_id.asc()).all()
    return [WaktuBimbinganSchema.model_validate(waktu) for waktu in waktu_list]


async def update_waktu_bimbingan(db: Session, bimbingan_id: str, _data: UpdateWaktuBimbinganSchema):
    record = db.query(WaktuBimbingan).filter(WaktuBimbingan.bimbingan_id == bimbingan_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Waktu bimbingan tidak ditemukan")
    
    update_data = _data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    payload = {
        "event": "update_waktu_bimbingan",
        "bimbingan_id": bimbingan_id,
        "updated_data": update_data
    }

    await manager.broadcast_all(message=payload)

    return record


def delete_waktu_bimbingan(db: Session, bimbingan_id: str):
    _data = db.query(WaktuBimbingan).filter(WaktuBimbingan.bimbingan_id == bimbingan_id).first()
    if not _data:
        raise HTTPException(
            status_code=404,
            detail="Data tidak ditemukan"
        )

    db.delete(_data)
    db.commit()

    return {
        "message": f"Jadwal Bimbingan telah dihapus"
    }

def generate_bimbingan_id(db: Session, dosen_inisial: str) -> str:
    count = db.query(WaktuBimbingan).filter(WaktuBimbingan.dosen_inisial == dosen_inisial).count()
    new_id = f"{dosen_inisial}{count+1}"
    return new_id
