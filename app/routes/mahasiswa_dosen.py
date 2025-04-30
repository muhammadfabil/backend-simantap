from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.schemas.mahasiswa_dosen import *
from app.services.relasi_service import *

from app.database.session import get_db

router = APIRouter(prefix="/relation", tags=["Mahasiswa-Dosen"])

@router.post("/", response_model=MahasiswaDosenSchema)
def create_relation(relation: MahasiswaDosenCreateSchema, db: Session = Depends(get_db)):
    return assign_dosen(db, relation)

@router.get("/", response_model=list[MahasiswaDosenSchema])
def get_all_relation(db: Session = Depends(get_db)):
    return get_relation(db)

@router.get("/mahasiswa/{nim}", response_model=list[MahasiswaDosenSchema])
def get_all_relation_by_mahasiswa(nim:str, db: Session = Depends(get_db)):
    return get_relation_by_mahasiswa(db, nim)

@router.get("/dosen/{alias}")
def get_all_relation_by_dosen(alias:str, db: Session = Depends(get_db)):
    relations = get_relation_by_dosen(db, alias)

    daftar_mahasiswa = []
    for relation in relations:
        if relation.mahasiswa:
            daftar_mahasiswa.append({
                "id": relation.id,
                "nama": relation.mahasiswa.nama,
                "nim": relation.mahasiswa.nim,
                "role": relation.role
            })
            
    return {
        "Daftar Mahasiswa": daftar_mahasiswa
        }

@router.put("/{id}", response_model=MahasiswaDosenSchema)
def edit_relation(id:int, update:MahasiswaDosenUpdateSchema, db: Session = Depends(get_db)):
    return update_relation(db, id, update)
    
@router.delete("/{id}", response_model=MahasiswaDosenSchema)
def delete_relation(id:int, db: Session = Depends(get_db)):
    return delete_relation_by_id(db, id)