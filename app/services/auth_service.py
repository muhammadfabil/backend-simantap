from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.middleware.jwt_handler import create_access_token
from app.middleware.jwt_handler import create_refresh_token
from app.middleware.jwt_handler import create_reset_token
from app.middleware.jwt_handler import decode_access_token
from app.middleware.jwt_handler import hash_password
from app.middleware.jwt_handler import verify_reset_token
from app.middleware.jwt_handler import verify_password
from app.middleware.smtp_sender import send_reset_password_email

from app.database.models.admin import Admin
from app.database.models.dosen import Dosen
from app.database.models.mahasiswa import Mahasiswa
from app.database.models.user import User

from app.schemas.user import AdminProfile
from app.schemas.user import DosenProfile
from app.schemas.user import MahasiswaProfile
from app.schemas.user import TokenResponse
from app.schemas.user import UserProfileResponse

def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    userID = user.user_id    
    access_token = create_access_token(
        data={
            "sub": str(userID),
            "role": user.role
        }
    )
    refresh_token = create_refresh_token(
        data={
            "sub": str(userID),
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def refresh_access_token(db: Session, token: str) -> TokenResponse:
    payload = decode_access_token(token)
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid Token Type",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user_id: str = payload.get("sub")
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User Not Found",
            headers={"WWW-Authenticate":"Bearer"}
        )
    access_token = create_access_token(
        data={"sub": str(user.user_id), "role": user.role},
    )
    new_refresh_token = create_refresh_token(
        data={"sub": str(user.user_id), "role": user.role},
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )

def logout_user():
    pass

def get_user_profile(user: User, db: Session) -> UserProfileResponse:
    match user.role:
        case "admin":
            admin = db.query(Admin).filter(Admin.id == user.user_id).first()
            profile = AdminProfile(role="admin", name=admin.name, email=admin.email)
        case "dosen":
            dosen = db.query(Dosen).filter(Dosen.id == user.user_id).first()
            profile = DosenProfile(role="dosen", name=dosen.name, alias=dosen.alias, email=dosen.email)
        case "mahasiswa":
            mhs = db.query(Mahasiswa).filter(Mahasiswa.id == user.user_id).first()
            profile = MahasiswaProfile(role="mahasiswa", name=mhs.nama, nim=mhs.nim, email=mhs.email)
        case _:
            raise HTTPException(status_code=400, detail="Invalid user role")
        
    return UserProfileResponse(
        user_id=user.user_id,
        email=user.email,
        role=user.role,
        profile=profile
    )

def decode_token_and_get_user(token: str, db: Session) -> User:
    payload = decode_access_token(token)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Authentication Credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User Not Found",
            headers={"WWW-Authenticate":"Bearer"}
        )
    return user

def forgot_password(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User Not Found",
            headers={"WWW-Authenticate":"Bearer"}
        )
    reset_token = create_reset_token(email)
    send_reset_password_email(email, reset_token) 
    return {"message": "Reset link has been sent to your email"}

def reset_password(db: Session, token: str, new_password: str):
    email = verify_reset_token(token)
    if not email:
        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired Token",
            headers={"WWW-Authenticate":"Bearer"}
        )

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User Not Found",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
    hashed_password = hash_password(new_password)
    user.password = hashed_password
    
    if user.role == "mahasiswa":
        mhs = db.query(Mahasiswa).filter(Mahasiswa.id == user.user_id).first()
        mhs.password = hashed_password
    elif user.role == "dosen":
        dosen = db.query(Dosen).filter(Dosen.id == user.user_id).first()
        dosen.password = hashed_password
    elif user.role == "admin":
        admin = db.query(Admin).filter(Admin.id == user.user_id).first()
        admin.password = hashed_password
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid User Role",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
    db.commit()
    db.refresh(user)

    return {"message": "Password has been reset successfully"}