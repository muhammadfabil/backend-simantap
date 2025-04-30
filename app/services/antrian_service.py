from fastapi import HTTPException
from fastapi import UploadFile

from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from app.database.models.antrian_bimbingan import AntrianBimbingan
from app.database.models.waktu_bimbingan import WaktuBimbingan

from app.schemas.antrian_bimbingan import *

from app.routes.file import upload_file
from app.routes.websocket_router import manager

from datetime import datetime
from uuid import uuid4

import asyncio

def get_antrian_by_id(db: Session, id_antrian: UUID):
    return db.query(AntrianBimbingan)\
        .options(joinedload(AntrianBimbingan.files))\
        .filter(AntrianBimbingan.id_antrian == id_antrian)\
        .first()

async def ambil_antrian_bimbingan(db: Session, waktu_id: str, nim: str, file: Optional[UploadFile] = None):
    waktu = db.query(WaktuBimbingan).filter(WaktuBimbingan.bimbingan_id == waktu_id).first()
    if not waktu:
        raise HTTPException(
            status_code=404,
            detail="Waktu bimbingan tidak ditemukan."
        )
    
    dosen = waktu.dosen
    
    sudah_ada = db.query(AntrianBimbingan).filter_by(mahasiswa_nim=nim, waktu_id=waktu_id).first()
    if sudah_ada:
        raise HTTPException(
            status_code=400,
            detail="Anda sudah masuk antrian."
        )
    
    jumlah = db.query(AntrianBimbingan).filter_by(waktu_id=waktu_id).count()
    if jumlah >= waktu.jumlah_antrian:
        raise HTTPException(
            status_code=400,
            detail="Slot penuh."
        )
    
    posisi = jumlah + 1
    
    antrianId = uuid4()
    antrian = AntrianBimbingan(
        id_antrian = antrianId,
        mahasiswa_nim = nim,
        waktu_id = waktu_id,
        dosen_inisial = waktu.dosen_inisial,
        status_antrian = "Menunggu",
        position = posisi,
        created_at = datetime.now()
    )
    db.add(antrian)
    db.commit()
    db.refresh(antrian)

    daftar = db.query(AntrianBimbingan).filter_by(waktu_id=waktu_id).order_by(AntrianBimbingan.created_at).all()

    uploaded_file = None
    if file:
        uploaded_file = await upload_file(
            antrian_id = antrianId,
            mahasiswa_nim = nim,
            file = file,
            db = db
        )

    queue_data = [
        {
            "id_antrian": str(item.id_antrian),
            "nim": item.mahasiswa_nim,
            "status": item.status_antrian
        }
        for item in daftar
    ]

    payload = {
        "event": "update_antrian",
        "inisial": dosen.alias,
        "waktu_id": waktu.bimbingan_id,
        "tanggal": str(waktu.tanggal),
        "queue": queue_data
    }

    send_tasks = [
    manager.send_json(user_id=item.mahasiswa_nim, data=payload)
    for item in daftar
    ]

    send_tasks.append(
        manager.send_json(user_id=dosen.alias, data=payload)
    )

    await asyncio.gather(*send_tasks)

    return AmbilAntrianResponse(
        message="Berhasil masuk antrian",
        posisi=posisi,
        id_antrian=antrian.id_antrian,
        antrian=AmbilAntrianSchema(
            mahasiswa_nim=antrian.mahasiswa_nim,
            waktu_id=antrian.waktu_id
    ),
    files=FileSchema.model_validate(uploaded_file) if uploaded_file else None
)

async def notify_position_change(nim: str, position: int):
    await manager.send_message(nim, f"Posisi Anda di antrian: {position}")

async def update_status_antrian(db: Session, id_antrian: UUID):
    antrian = db.query(AntrianBimbingan).filter_by(id_antrian=id_antrian).first()

    if not antrian:
        raise HTTPException(
            status_code=404,
            detail="Antrian tidak ditemukan."
        )

    original_status = antrian.status_antrian

    if antrian.status_antrian == "Menunggu":
        antrian.status_antrian = "Dalam Bimbingan"
    elif antrian.status_antrian == "Dalam Bimbingan":
        antrian.status_antrian = "Selesai"
    
    db.commit()
    db.refresh(antrian)

    waktu = db.query(WaktuBimbingan).filter(WaktuBimbingan.bimbingan_id == antrian.waktu_id).first()

    if waktu and original_status == "Dalam Bimbingan":
        already_in_progress = db.query(AntrianBimbingan).filter_by(
            waktu_id=waktu.bimbingan_id,
            status_antrian="Dalam Bimbingan"
        ).first()

        if not already_in_progress:
            next_position = antrian.position + 1

            next_antrian = db.query(AntrianBimbingan).filter_by(
                waktu_id=waktu.bimbingan_id,
                position=next_position,
                status_antrian="Menunggu"
            ).first()

            if next_antrian:
                next_antrian.status_antrian = "Dalam Bimbingan"
                db.commit()
                db.refresh(next_antrian)

    if waktu:
        daftar = db.query(AntrianBimbingan).filter_by(
            waktu_id=waktu.bimbingan_id
        ).order_by(AntrianBimbingan.position).all()

        payload = {
            "event": "update_antrian",
            "inisial": antrian.dosen_inisial,
            "waktu_id": waktu.bimbingan_id,
            "tanggal": str(waktu.tanggal),
            "queue": [
                {
                    "id_antrian": str(item.id_antrian),
                    "nim": item.mahasiswa_nim,
                    "status": item.status_antrian
                } for item in daftar
            ]
        }

        send_tasks = [
            manager.send_json(user_id=item.mahasiswa_nim, data=payload)
            for item in daftar
        ]

        # Kirim ke dosennya juga
        send_tasks.append(
            manager.send_json(user_id=antrian.dosen_inisial, data=payload)
        )

        await asyncio.gather(*send_tasks)

    return {"message": f"Status antrian diperbaharui menjadi {antrian.status_antrian}."}

def delete_antrian(idAntrian: UUID, db: Session):
    _data = db.query(AntrianBimbingan).filter(AntrianBimbingan.id_antrian == idAntrian).first()
    if not _data:
        raise HTTPException(
            status_code=404,
            detail="Data tidak ditemukan"
        )

    db.delete(_data)
    db.commit()

    return {
        "message": f"Antrian telah dihapus"
    }