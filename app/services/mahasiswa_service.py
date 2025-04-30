from fastapi import HTTPException
from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.schemas.mahasiswa import *
from app.database.models.mahasiswa import Mahasiswa
from app.database.models.user import User
from app.database.models.mahasiswa_dosen import MahasiswaDosen
from app.middleware.jwt_handler import hash_password
from app.middleware.supabase_client import SupabaseClient

import uuid
supabase = SupabaseClient()

def create_mahasiswa(db: Session, mahasiswa: MahasiswaSchema):
    hashed_password = hash_password(mahasiswa.password) 
    mahasiswa_id = uuid.uuid4()
    
    db_mahasiswa = Mahasiswa(
        id=mahasiswa_id,
        nim=mahasiswa.nim,
        nama=mahasiswa.nama,
        email=mahasiswa.email,
        password=hashed_password
    )
    db.add(db_mahasiswa)
    db.commit()
    db.refresh(db_mahasiswa)

    db_user = User(
        user_id = mahasiswa_id,
        email = mahasiswa.email,
        password = hashed_password,
        role = "mahasiswa"
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_mahasiswa

def get_mahasiswa(db: Session, nim: str):
    return db.query(Mahasiswa).filter(Mahasiswa.nim == nim).first()

def get_all_mahasiswa(db: Session):
    return db.query(Mahasiswa).order_by(Mahasiswa.nim.asc()).all()

def get_detail_mahasiswa(db: Session, id: UUID):
    return db.query(Mahasiswa).filter(Mahasiswa.id == id).first()

def get_mahasiswa_detail(db: Session, nim:str):
    return (
        db.query(Mahasiswa)
        .options(
            joinedload(Mahasiswa.dosen_relation).joinedload(MahasiswaDosen.dosen),
            joinedload(Mahasiswa.antrian_bimbingan)
        )
        .filter(Mahasiswa.nim == nim)
        .first()
    )

def update_mahasiswa(db: Session, nim: str, mahasiswa_data: MahasiswaUpdateSchema, avatar: Optional[UploadFile] = None):
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.nim == nim).first()
    if not mahasiswa:
        return None
    
    update_data = mahasiswa_data.model_dump(exclude_unset=True)
    if avatar:
        avatar_url = supabase.upload_to_supabase(avatar, folder="mahasiswa")
        update_data["avatar_url"] = avatar_url

    user = db.query(User).filter(User.user_id == mahasiswa.id).first()
    if user:
        if "email" in update_data and update_data["email"] is not None:
            user.email = update_data["email"]

        db.commit()
        db.refresh(user)
    
    for key, value in update_data.items():
        if value is not None:
            if isinstance(value, str):
                value = value.strip()
            setattr(mahasiswa, key, value)

    db.commit()
    db.refresh(mahasiswa)
    return mahasiswa

def delete_mahasiswa(db: Session, mahasiswa_id: UUID):
    _data = db.query(Mahasiswa).filter(Mahasiswa.id == mahasiswa_id).first()
    if not _data:
        raise HTTPException(
            status_code=404,
            detail="Data Mahasiswa Tidak Ditemukan"
        )

    name = _data.nama
    user_data = db.query(User).filter(User.user_id == mahasiswa_id).first()
    if user_data:
        db.delete(user_data)

    db.delete(_data)
    db.commit()

    return {
        "message": f"Data Mahasiswa {name} telah dihapus"
    }