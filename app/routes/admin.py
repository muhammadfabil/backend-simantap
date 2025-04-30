from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.services.admin_service import *
from app.schemas.admin import *
from app.middleware.security import require_roles

from uuid import UUID

from app.database.session import get_db

router = APIRouter(
    prefix="/admin", 
    tags=["Admin"],
    dependencies=[Depends(require_roles("admin"))])

@router.post("/", response_model=AdminSchema)
def create_admin_route(admin: AdminCreateSchema, db: Session = Depends(get_db)):
    return create_admin(db, admin)

@router.get("/all", response_model=List[AdminSchema])
def get_all_admin_route(db: Session = Depends(get_db)):
    return get_all_admin(db)

@router.get("/{admin_id}", response_model=AdminSchema)
def get_admin_route(admin_id: UUID, db: Session = Depends(get_db)):
    return get_admin_by_id(db, admin_id)

@router.put("/{admin_id}", response_model=AdminSchema)
def update_admin_route(admin_id: UUID, data:AdminUpdateSchema, db: Session = Depends(get_db)):
    return update_admin(db, admin_id, data)

@router.delete("/{admin_id}")
def delete_admin_route(admin_id: UUID, db: Session = Depends(get_db)):
    return delete_admin(db, admin_id)

@router.get("/e/{email}", response_model=AdminSchema)
def get_admin_by_email_route(email: str, db: Session = Depends(get_db)):
    return get_admin_by_email(db, email)