from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.database.models.mahasiswa_dosen import MahasiswaDosen
from app.database.models.mahasiswa import Mahasiswa

from app.schemas.mahasiswa_dosen import *

from fastapi import HTTPException

ROLE_MAPPING = {
    "wali"  : ("Dosen Wali", 1),
    "kp"    : ("Dosen KP", 1),
    "pbb1"  : ("Dosen Pembimbing 1", 1),
    "pbb2"  : ("Dosen Pembimbing 2", 1),
    "pj1"   : ("Dosen Penguji 1", 1),
    "pj2"   : ("Dosen Penguji 2", 1),
}

def assign_dosen(db: Session, assigment: MahasiswaDosenSchema):
    role_key = assigment.role.lower()

    # Validasi role
    if role_key not in ROLE_MAPPING:
        raise HTTPException(status_code=400, detail="Role tidak sesuai")

    role_group, max_allowed = ROLE_MAPPING[role_key]

    # Hitung jumlah role yang sama
    existing_count = db.query(MahasiswaDosen).filter(
        MahasiswaDosen.mahasiswa_nim == assigment.mahasiswa_nim,
        MahasiswaDosen.role == role_group
    ).count()

    if existing_count >= max_allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Maksimal {max_allowed} {role_group}"
        )
    
    assigment.role = role_group

    new_assignment = MahasiswaDosen(**assigment.model_dump())
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment

def get_relation(db: Session):
    return db.query(MahasiswaDosen).join(Mahasiswa).all()

def get_relation_by_mahasiswa(db: Session, nim: str):
    return db.query(MahasiswaDosen).filter(MahasiswaDosen.mahasiswa_nim == nim).all()

def get_relation_by_dosen(db: Session, alias: str):
    return (
        db.query(MahasiswaDosen)
        .options(joinedload(MahasiswaDosen.mahasiswa))
        .filter(MahasiswaDosen.dosen_alias == alias)
        .all()
    )

def update_relation(db: Session, id: int, updated: MahasiswaDosenUpdateSchema):
    relation = db.query(MahasiswaDosen).filter(MahasiswaDosen.id == id).first()
    if not relation:
        raise HTTPException(status_code=404, detail="Relasi tidak Ditemukan")

    update_data = updated.model_dump(exclude_unset=True)

    # Handle role validation if role is updated
    if "role" in update_data:
        role_key = update_data["role"].lower()

        if role_key not in ROLE_MAPPING:
            raise HTTPException(status_code=400, detail="Role tidak sesuai")

        role_group, max_allowed = ROLE_MAPPING[role_key]

        existing_count = db.query(MahasiswaDosen).filter(
            MahasiswaDosen.mahasiswa_nim == relation.mahasiswa_nim,
            MahasiswaDosen.role == role_group,
            MahasiswaDosen.id != id  # exclude current record from the count
        ).count()

        if existing_count >= max_allowed:
            raise HTTPException(
                status_code=400,
                detail=f"Maksimal {max_allowed} {role_group}"
            )
        
        update_data["role"] = role_group

    for key, value in update_data.items():
        setattr(relation, key, value)

    db.commit()
    db.refresh(relation)
    return relation


def delete_relation_by_id(db: Session, id:int):
    relation = db.query(MahasiswaDosen).filter(MahasiswaDosen.id == id).first()
    if not relation:
        raise HTTPException(
            status_code=404,
            detail="Relasi tidak Ditemukan"
        )
    db.delete(relation)
    db.commit()
    return relation
