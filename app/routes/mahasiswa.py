from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from uuid import UUID

from app.services.mahasiswa_service import *
from app.schemas.mahasiswa import *

from app.database.session import get_db
from app.database.models.antrian_bimbingan import AntrianBimbingan
from app.middleware.security import require_roles

router = APIRouter(prefix="/mahasiswa", tags=["Mahasiswa"])

@router.post("/", response_model=MahasiswaCreateSchema)
def create_mahasiswa_route(mahasiswa: MahasiswaResponseSchema, db: Session = Depends(get_db)):
    return create_mahasiswa(db, mahasiswa)

@router.get("/all", response_model=list[MahasiswaCreateSchema])
def get_all_mahasiswa_route(db: Session = Depends(get_db)):
    return get_all_mahasiswa(db)

@router.get("/{nim}", response_model=MahasiswaSchema)
def get_mahasiswa_route(nim: str, db: Session = Depends(get_db)):
    return get_mahasiswa(db, nim)

@router.get("/admin/{id}", response_model=MahasiswaSchema)
def get_detail_mahasiswa_route(id: UUID, db: Session = Depends(get_db)):
    return get_detail_mahasiswa(db, id)

@router.put("/{nim}")
def update_mahasiswa_route(
    nim: str, 
    nama: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    topik_penelitian: Optional[str] = Form(None),
    semester_saat_ini: Optional[int] = Form(None),
    status_mahasiswa: Optional[str] = Form(None),
    avatar: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    update_data = MahasiswaUpdateSchema(
        nama=nama,
        email=email,
        password=password,
        topik_penelitian=topik_penelitian,
        semester_saat_ini=semester_saat_ini,
        status_mahasiswa=status_mahasiswa,
    )

    data = update_mahasiswa(db, nim, update_data, avatar)
    if not data:
        raise HTTPException(status_code = 404, detail = "Mahasiswa Tidak Ditemukan")
    return {"Message": "Mahasiswa Telah diUpdate"}

@router.get("/detail/{nim}")
def get_mahasiswa_detail_route(nim: str, db: Session = Depends(get_db)):
    mahasiswa = get_mahasiswa_detail(db, nim)
    if not mahasiswa:
        raise HTTPException(
            status_code=404,
            detail="Mahasiswa not Found"
        )
    
    antrian_bimbingan_records = db.query(AntrianBimbingan).filter(AntrianBimbingan.mahasiswa_nim == nim).all()

    antrian_bimbingan_count_by_dosen = {}
    for antrian in antrian_bimbingan_records:
        dosen_alias = antrian.dosen_inisial
        if dosen_alias not in antrian_bimbingan_count_by_dosen:
            antrian_bimbingan_count_by_dosen[dosen_alias] = 0
        antrian_bimbingan_count_by_dosen[dosen_alias] += 1

    dosen_roles = {
        "Dosen Wali": None,
        "Dosen KP": None,
        "Dosen Pembimbing 1": None,
        "Dosen Pembimbing 2": None,
        "Dosen Penguji 1": None,
        "Dosen Penguji 2": None
    }

    for relasi in mahasiswa.dosen_relation:
        if relasi.dosen:
            role = relasi.role
            dosen_roles[role] = {
                "nama": relasi.dosen.name,
                "alias": relasi.dosen.alias
            }

    bimbingan = []    
    for antrian in mahasiswa.antrian_bimbingan:
        bimbingan.append({
            "id_antrian": str(antrian.id_antrian),
            "dosen_inisial": antrian.dosen_inisial,
            "status_antrian": antrian.status_antrian
        })

    response = {
        "mahasiswa": {
            "id": str(mahasiswa.id),
            "nama": mahasiswa.nama,
            "nim": mahasiswa.nim,
            "email": mahasiswa.email,
            "tugas_akhir": {
                "judul": mahasiswa.topik_penelitian,
                "status": "Belum Ditentukan"
            }
        },
        "mahasiswa_dosen": dosen_roles,
        "bimbingan": bimbingan,
        "jumlah_bimbingan": len(mahasiswa.antrian_bimbingan),
        "jumlah_bimbingan_by_dosen": antrian_bimbingan_count_by_dosen
    }

    return JSONResponse(content=response)

@router.delete("/del/{mahasiswa_id}", dependencies=[Depends(require_roles("admin"))])
def delete_mahasiswa_route(mahasiswa_id: UUID, db: Session = Depends(get_db)):
    return delete_mahasiswa(db, mahasiswa_id)