from typing import Dict
import json

from fastapi.testclient import TestClient

from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud import crud_user as crud
from app.crud import crud_organizations as org_crud
from app.tests.utils.utils import random_lower_string


def test_invite_new_user(client: TestClient, db: Session, superuser_token_headers: Dict[str, str]) -> None:
    dim_org = org_crud.get_by_name(db, "DIM")
    assert dim_org

    payload = {
        "email": settings.TEST_USER_EMAIL,
        "organization": dim_org.id
    }

    r = client.post(f"{settings.API_V1_STR}/users/invite", json=payload, headers=superuser_token_headers)

    assert 200 <= r.status_code < 300
    invited_user = r.json()
    user = crud.get_by_email(db, email=settings.TEST_USER_EMAIL)
    assert user
    assert user.email == invited_user["email"]
    assert user.email_confirmed == False
    assert user.is_active == False
    assert user.role == "aid_worker"


def test_confirm_user_invite(client: TestClient, db: Session) -> None:
    test_user_registration_token = crud.get_by_email(db, email=settings.TEST_USER_EMAIL).registration_token
    assert test_user_registration_token

    payload = {
        "email": settings.TEST_USER_EMAIL,
        "password": settings.TEST_USER_PASSWORD,
        "username": "Test",
        "full_name": "Test User"
    }

    r = client.post(f"{settings.API_V1_STR}/users/confirm-registration?access_token={test_user_registration_token}",
                    data=json.dumps(payload))

    assert 200 <= r.status_code < 300
    registered_user = r.json()
    user = crud.get_by_email(db, email=settings.TEST_USER_EMAIL)
    assert user
    assert user.username == registered_user['username']
    assert user.email_confirmed == True
    assert user.is_active == True


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

    payload = {
        "old_password": new_password,
        "new_password": settings.TEST_USER_PASSWORD
    }

    r = client.put(f"{settings.API_V1_STR}/users/password", data=json.dumps(payload), headers=aid_worker_token_headers)
    assert 200 <= r.status_code < 300


def test_user_delete_me(client: TestClient, db: Session, aid_worker_token_headers: Dict[str, str]) -> None:

    r = client.delete(f"{settings.API_V1_STR}/users/delete-me", headers=aid_worker_token_headers)
    assert 200 <= r.status_code < 300

    user = crud.get_by_email(db, email=settings.TEST_USER_EMAIL)
    assert user is None
