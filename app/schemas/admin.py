from pydantic import BaseModel
from typing import Optional
from uuid import UUID
class AdminSchema(BaseModel):
    id: UUID
    name: str
    email: str
    # password: str
    
    class Config:
        from_attributes = True

class AdminCreateSchema(BaseModel):
    name: str
    email: str
    password: str

class AdminUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    # password: Optional[str] = None
