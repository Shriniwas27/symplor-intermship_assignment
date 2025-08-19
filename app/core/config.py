from typing import List
from pydantic_settings import BaseSettings
import json


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    environment: str = "production"
    backend_cors_origins: List[str] = []
    default_admin_email: str = "admin@company.com"
    default_admin_password: str = "admin123"

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @classmethod
    def parse_cors_origins(cls, origins):
        if isinstance(origins, str):
            try:
                return json.loads(origins)
            except Exception:
                return [s.strip() for s in origins.split(",")]
        return origins

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.backend_cors_origins = self.parse_cors_origins(self.backend_cors_origins)


settings = Settings()

