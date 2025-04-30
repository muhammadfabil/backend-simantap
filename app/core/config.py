from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    app_name: str = "Dosen Queue System API"
    cors_origins: List[str]
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    supabase_url: str
    supabase_key: str
    supabase_bucket: str
    vapid_private_key: str
    vapid_public_key: str
    access_token_expire_minutes: int = 60 
    timezone: str = "Asia/Jakarta"
    smtp_host: str
    smtp_port: int 
    smtp_user: str
    smtp_password: str
    frontend_url: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        extra = "allow"

load_dotenv()
settings = Settings()