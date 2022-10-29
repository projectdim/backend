from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud import crud_user as crud


def user_authentication_headers(*, client: TestClient, email: str, password: str) -> Dict[str, str]:

    data = {
        "username": email,
        "password": password
    }

    r = client.post(f"{settings.API_V1_STR}/auth/login/token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:

    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD
    }

    r = client.post(f"{settings.API_V1_STR}/auth/login/token", data=login_data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def get_superuser_id(db: Session) -> int:
    return crud.get_by_email(db, email=settings.FIRST_SUPERUSER).id


