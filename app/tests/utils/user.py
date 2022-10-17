from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


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


