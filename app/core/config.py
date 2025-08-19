from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    environment: str = "development"
    backend_cors_origins: List[str] = []
    default_admin_email: str = "admin@company.com"
    default_admin_password: str = "admin123"
    
    class Config:
        env_file = ".env"

settings = Settings()
