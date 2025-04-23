import os
from pydantic_settings import BaseSettings
from typing import Optional, List
import secrets
import dotenv

dotenv.load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "FiBook API"
    API_V1_STR: str = "/api/v1"

    # Database
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL")

    # JWT Token settings
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 8 * 60 * 60

    # First superuser
    FIRST_SUPERUSER_EMAIL: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"

    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
