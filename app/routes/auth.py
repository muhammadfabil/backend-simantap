from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.auth_service import *
from app.schemas.user import *
from app.middleware.security import *
from app.middleware.token_blacklist import add_token_to_blacklist

from app.database.session import get_db
from uuid import UUID

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/login", response_model=TokenResponse)
def login_route(login_data: LoginUser, db: Session = Depends(get_db)):
    return login_user(db, login_data.email, login_data.password)

@router.get("/me")
async def get_profile_route(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_profile(user, db)

@router.post("/refresh", response_model=TokenResponse)
def refresh_route(token: str, db: Session = Depends(get_db)):
    return refresh_access_token(db, token)

@router.post("/logout")
def logout_user(token: str = Depends(oauth2_scheme)):
    add_token_to_blacklist(token)
    return {"message": "Logout successful"}

@router.get("/test-me")
def get_me_test(token: str, db: Session = Depends(get_db)):
    user = decode_token_and_get_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@router.post("/forgot-password")
def forgot_password_route(email: str, db: Session = Depends(get_db)):
    return forgot_password(db, email)

@router.post("/reset-password")
def reset_password_route(
    token: str, 
    new_password: str, 
    db: Session = Depends(get_db)
):
    return reset_password(db, token, new_password)