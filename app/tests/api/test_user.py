from typing import Dict
import json

from fastapi.testclient import TestClient

from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud import crud_user as crud
from app.tests.utils.utils import random_lower_string


def test_create_new_user(client: TestClient, db: Session, superuser_token_headers: Dict[str, str]) -> None:

    payload = {
        "email": settings.TEST_USER_EMAIL,
        "password": settings.TEST_USER_PASSWORD,
        "username": "Test",
        "full_name": "Test account"
    }

    r = client.post(f"{settings.API_V1_STR}/users/register", json=payload, headers=superuser_token_headers)

    assert 200 <= r.status_code < 300
    registered_user = r.json()
    user = crud.get_by_email(db, email=settings.TEST_USER_EMAIL)
    assert user
    assert user.email == registered_user["email"]


def test_get_me(client: TestClient, aid_worker_token_headers: Dict[str, str]) -> None:

    r = client.get(f"{settings.API_V1_STR}/users/me", headers=aid_worker_token_headers)

    current_user = r.json()
    assert current_user
    assert current_user["email"] == settings.TEST_USER_EMAIL


def test_patch_user(client: TestClient, db: Session, aid_worker_token_headers: Dict[str, str]) -> None:

    existing_user = crud.get_by_email(db, email=settings.TEST_USER_EMAIL)

    payload = {
        "username": random_lower_string(),
        "email": existing_user.email,
        "full_name": existing_user.full_name
    }

    r = client.put(f"{settings.API_V1_STR}/users/info", json=payload, headers=aid_worker_token_headers)
    updated_user = r.json()
    assert updated_user
    assert updated_user["username"] != existing_user.username


def test_patch_user_password(client: TestClient, db: Session, aid_worker_token_headers: Dict[str, str]) -> None:

    new_password = random_lower_string()

    payload = {
        "old_password": settings.TEST_USER_PASSWORD,
        "new_password": new_password
    }

    r = client.put(f"{settings.API_V1_STR}/users/password", data=json.dumps(payload), headers=aid_worker_token_headers)
    assert 200 <= r.status_code < 300

    incorrect_login_payload = {
        "username": settings.TEST_USER_EMAIL,
        "password": settings.TEST_USER_PASSWORD
    }

    incorrect_login_request = client.post(f"{settings.API_V1_STR}/auth/login/token", data=incorrect_login_payload)
    assert incorrect_login_request.status_code == 400
    assert "access_token" not in incorrect_login_request.json()

    correct_login_payload = {
        "username": settings.TEST_USER_EMAIL,
        "password": new_password
    }

    correct_login_request = client.post(f"{settings.API_V1_STR}/auth/login/token", data=correct_login_payload)
    token = correct_login_request.json()
    assert correct_login_request.status_code == 200
    assert "access_token" in token
    assert token["access_token"]

