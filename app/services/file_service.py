from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.models.file import Files
from app.schemas.file import *
from app.middleware.supabase_client import *

from uuid import UUID

def get_files(db: Session, student_id: str):
    return db.query(Files).filter(Files.mahasiswa_nim == student_id).all()

def update_files(db: Session, file_id: UUID, update_data: FileUpdateSchema):
    file_db = db.query(Files).filter(Files.file_id == file_id).first()

    if not file_db:
        raise HTTPException(status_code=404, detail="File Not Found.")
    
    update_data_dict = update_data.model_dump(exclude_unset=True)

    if not update_data_dict:
        raise HTTPException(status_code=400, detail="No data provided to update")

    for key, value in update_data_dict.items():
        setattr(file_db, key, value)

    file_db.update_at = datetime.now()
    db.commit()
    db.refresh(file_db)
    return file_db