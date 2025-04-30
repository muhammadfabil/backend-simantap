from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import UploadFile

from sqlalchemy.orm import Session

from app.services.layanan_service import *
from app.schemas.layanan import * 
from app.middleware.security import require_roles 
from app.database.session import get_db
from app.middleware.supabase_client import SupabaseClient

router = APIRouter(prefix="/layanan", tags=["Layanan"])
supabase = SupabaseClient()

# ============================
# JENIS LAYANAN
# ============================


@router.post("/jenis", response_model=JenisLayananResponse, dependencies=[Depends(require_roles("admin"))])
def create_jenis_layanan_route(data: JenisLayananCreate, db: Session = Depends(get_db)):
    return create_jenis_layanan(db, data)

@router.get("/jenis", response_model=list[JenisLayananResponse])
def get_all_jenis_layanan_route(db: Session = Depends(get_db)):
    return get_all_jenis_layanan(db)

@router.get("/jenis/{id}", response_model=JenisLayananResponse)
def get_jenis_layanan_by_id_route(id: int, db: Session = Depends(get_db)):
    jenis = get_jenis_layanan_by_id(db, id)
    if not jenis:
        raise HTTPException(
            status_code=404,
            detail="Jenis Layanan tidak Ditemukan"
        )
    return jenis

@router.put("/jenis/{id}", response_model=JenisLayananResponse)
def update_jenis_route(id: int, data: JenisLayananCreate, db: Session = Depends(get_db)):
    result = update_jenis_layanan(db, id, data)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Jenis Layanan tidak Ditemukan"
        )
    return result

@router.delete("/jenis/{id}")
def delete_jenis_route(id: int, db: Session = Depends(get_db)):
    if not delete_jenis_layanan(db, id):
        raise HTTPException(
            status_code=404,
            detail="Jenis Layanan tidak Ditemukan"
        )
    return {
        "message": "Jenis Layanan berhasil dihapus"
    }


# ============================
# DOKUMEN PERSYARATAN
# ============================


@router.post("/dokumen", response_model=DokumenPersyaratanResponse)
def create_dokumen_route(data: DokumenPersyaratanCreate, db: Session = Depends(get_db)):
    return create_dokumen(db, data)

@router.get("/dokumen/{jenis_layanan_id}", response_model=list[DokumenPersyaratanResponse])
def get_dokumen_by_jenis_route(jenis_laynan_id: int, db: Session = Depends(get_db)):
    return get_dokumen_by_jenis_layanan(db, jenis_laynan_id)

@router.delete("/dokumen/{id}")
def delete_dokumen_route(id: int, db: Session = Depends(get_db)):
    if not delete_dokumen(db, id):
        raise HTTPException(
            status_code=404,
            detail="Dokumen tidak Ditemukan"
        )
    return{
        "message": "Dokumen berhasil dihapus"
    }


# ============================
# PENGAJUAN LAYANAN
# ============================


@router.post("/pengajuan", response_model=PengajuanLayananResponse)
def create_pengajuan_route(data: PengajuanLayananCreate, db: Session = Depends(get_db)):
    return create_pengajuan(db, data)

@router.get("/pengajuan/all", response_model=list[PengajuanLayananResponse])
def get_all_pengajuan_route(db: Session = Depends(get_db)):
    return get_all_pengajuan(db)

@router.get("/pengajuan/{mahasiswa_nim}", response_model=list[PengajuanLayananResponse])
def get_pengajuan_by_nim(mahasiswa_nim: str, db: Session = Depends(get_db)):
    return get_pengajuan_by_mahasiswa(db, mahasiswa_nim)

@router.put("/pengajuan/{id}", response_model=PengajuanLayananResponse)
async def update_pengajuan_status_route(id: UUID, data: PengajuanUpdateSchema, db: Session = Depends(get_db)):
    result = update_status_pengajuan(db, id, data)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Pengajuan tidak Ditemukan"
        )

    return result


# ============================
# LAMPIRAN PENGAJUAN
# ============================


@router.post("/lampiran", response_model=LampiranPengajuanResponse)
def create_lampiran_route(data: LampiranPengajuanCreate, db: Session = Depends(get_db)):
    return create_dokumen(db, data)

@router.get("/lampiran/{pengajuan_id}", response_model=list[LampiranPengajuanResponse])
def get_lampiran_by_pengajuan_route(pengajuan_id: int, db: Session = Depends(get_db)):
    return get_lampiran_by_pengajuan(db, pengajuan_id)


# ============================
# UPLOAD LAMPIRAN
# ============================


@router.post("/upload/{pengajuan_id}")
def upload_lampiran(pengajuan_id: UUID, file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_url = supabase.upload_to_supabase(file, folder="lampiran")
    metadata = save_uploaded_file_metadata(db, file.filename, file_url, pengajuan_id)
    return {
        "message": "Upload Berhasil",
        "url": file_url,
        "metadata": metadata
    }


# ============================
# UPLOAD LAMPIRAN
# ============================

@router.post("/pengajuan/ajukan", response_model=PengajuanLayananResponse)
async def ajukan_layanan(
    mahasiswa_nim: str = Form(...),
    jenis_layanan_id: int = Form(...),
    berkas_utama: UploadFile = File(...),
    lampiran_tambahan: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    pengajuan = PengajuanLayanan(
        id = uuid.uuid4(),
        mahasiswa_nim = mahasiswa_nim,
        jenis_layanan_id = jenis_layanan_id,
        status = "Menunggu",
        created_at = datetime.now()
    )

    db.add(pengajuan)
    db.commit()
    db.refresh(pengajuan)

    payload = {
        "event": "new_pengajuan",
        "data": {
            "id": str(pengajuan.id),
            "status": pengajuan.status,
            "mahasiswa_nim": pengajuan.mahasiswa_nim,
            "created_at": pengajuan.created_at.isoformat()
        }
    }

    asyncio.create_task(
        manager.send_json(
            user_id="adminSiMantap",
            data=payload
        )
    )

    main_file_url = supabase.upload_to_supabase(berkas_utama, folder="pengajuan")
    save_uploaded_file_metadata(
        db=db,
        nama_dokumen=berkas_utama.filename,
        file_url=main_file_url,
        pengajuan_id=pengajuan.id
    )

    if lampiran_tambahan:
        lampiran_url = supabase.upload_to_supabase(lampiran_tambahan, folder="pengajuan")
        save_uploaded_file_metadata(
            db=db,
            nama_dokumen=lampiran_tambahan.filename,
            file_url=lampiran_url,
            pengajuan_id=pengajuan.id
        )

    return pengajuan