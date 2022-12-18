import secrets
import os

from typing import List, Optional, Any, Dict

from pydantic import BaseSettings, AnyHttpUrl, PostgresDsn, validator, EmailStr

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 10
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "PROJECTDIM")
    SERVER_NAME: str = os.getenv("SERVER_NAME", "Google Maps Project")
    SERVER_HOST: AnyHttpUrl = os.getenv("SERVER_HOST", "http://127.0.0.1:7000")
    DOMAIN_ADDRESS: AnyHttpUrl = os.getenv("DOMAIN_ADDRESS", "https://projectdim.org")

    CORS_ORIGINS: List[AnyHttpUrl] = []

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "admin")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}"
        )

    FIRST_SUPERUSER: EmailStr = os.getenv("SUPERUSER_EMAIL", "admin@admin.com")
    FIRST_SUPERUSER_PASSWORD = os.getenv("SUPERUSER_PASSWORD", "asd112233")

    TEST_USER_EMAIL: str = os.getenv("TEST_USER_EMAIL", "test@test.com")
    TEST_USER_PASSWORD: str = os.getenv("TEST_USER_PASSWORD", "asd112233")

    EMAILS_ENABLED: bool = os.getenv('EMAILS_ENABLED', True)
    AMAZON_APP_ID: str = os.getenv('AMAZON_APP_ID', "none")
    AWS_PROFILE: str = os.getenv("AWS_PROFILE", "dim")

    class Config:
        case_sensitive = True


settings = Settings()
