from fastapi.testclient import TestClient

from app.core.config import settings


def test_get_access_token(
        client: TestClient
) -> None:

    payload = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD
    }

    r = client.post(f"{settings.API_V1_STR}/auth/login/token", data=payload)

    token = r.json()
    assert r.status_code == 200
    assert "access_token" in token
    assert token["access_token"]
