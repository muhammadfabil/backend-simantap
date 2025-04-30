from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import HttpUrl

from typing import Literal 
from typing import Optional
from typing import Union

from uuid import UUID

class UserBase(BaseModel):
    email: str
    role: Literal["admin", "dosen", "mahasiswa"]

    model_config = ConfigDict(from_attributes=True)

class RegisterUser(UserBase):
    password: str

class LoginUser(BaseModel):
    email: str
    password: str

class UpdateProfile(BaseModel):
    full_name: Optional[str]
    avatar_utl: Optional[HttpUrl]
    ktm_url: Optional[HttpUrl]

    model_config = ConfigDict(from_attributes=True)

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class UserResponse(UserBase):
    id: UUID
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)

class AdminProfile(BaseModel):
    name: str

class DosenProfile(BaseModel):
    name: str
    inisial: str

class MahasiswaProfile(BaseModel):
    name: str
    nim: str

class BaseProfile(BaseModel):
    role: str
    email: str

class AdminProfile(BaseProfile):
    name: str

class DosenProfile(BaseProfile):
    name: str
    alias: str

class MahasiswaProfile(BaseProfile):
    name: str
    nim: str

# --- Unified User Response ---

class UserProfileResponse(BaseModel):
    user_id: UUID
    email: str
    role: str
    profile: Union[AdminProfile, DosenProfile, MahasiswaProfile]

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# class ResetPasswordSchema(BaseModel):
#     token: str
#     new_password: str

# class EmailSchema(BaseModel):
#     email: str