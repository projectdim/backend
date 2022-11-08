from typing import Dict

from fastapi.testclient import TestClient

from sqlalchemy.orm import Session

from app.crud import crud_organizations as crud
from app.core.config import settings


def test_create_organization(client: TestClient, db: Session, superuser_token_headers: Dict[str, str]) -> None:

    payload = {
        "name": "TestOrg"
    }

    r = client.post(f'{settings.API_V1_STR}/organizations/create', json=payload, headers=superuser_token_headers)
    assert 200 <= r.status_code < 300

    created_organization = r.json()
    assert created_organization
    organization = crud.get_by_id(db, organization_id=created_organization['id'])
    assert organization.name == created_organization["name"]


def test_get_all_organizations(client: TestClient, db: Session, superuser_token_headers: Dict[str, str]) -> None:

    r = client.get(f'{settings.API_V1_STR}/organizations/all', headers=superuser_token_headers)
    assert 200 <= r.status_code < 300


def test_get_organization_by_id(
        client: TestClient,
        db: Session,
        superuser_token_headers: Dict[str, str],
        master_organization_id: int
) -> None:

    r = client.get(f'{settings.API_V1_STR}/organizations/{master_organization_id}', headers=superuser_token_headers)
    assert 200 <= r.status_code < 300

    organization = r.json()
    assert organization["name"] == "DIM"
    assert organization["participants"]


def test_edit_organization(
        client: TestClient,
        db: Session,
        superuser_token_headers: Dict[str, str],
        master_organization_id: int
) -> None:

    payload = {
        "description": "Master organization",
        "website": "https://dim.org"
    }

    r = client.put(
        f'{settings.API_V1_STR}/organizations/{master_organization_id}/edit',
        json=payload,
        headers=superuser_token_headers
    )

    assert 200 <= r.status_code < 300

    response = r.json()
    assert response["website"] == "https://dim.org"


def test_remove_organization_member(
        client: TestClient,
        db: Session,
        superuser_token_headers: Dict[str, str],
        superuser_id: int,
        master_organization_id: int
) -> None:

    r = client.put(
        f'{settings.API_V1_STR}/organizations/{master_organization_id}/remove?user_id={superuser_id}',
        headers=superuser_token_headers
    )
    assert 200 <= r.status_code < 300

    organization = r.json()
    assert organization["participants"] == []


def test_invite_organization_members(
        client: TestClient,
        db: Session,
        superuser_token_headers: Dict[str, str],
        master_organization_id: int
) -> None:

    payload = {
        "emails": [settings.FIRST_SUPERUSER]
    }

    r = client.put(
        f'{settings.API_V1_STR}/organizations/{master_organization_id}/invite',
        json=payload,
        headers=superuser_token_headers
    )
    assert 200 <= r.status_code < 300

    organization = r.json()
    assert organization["participants"]
    assert organization["participants"][0]["email"] == settings.FIRST_SUPERUSER


def test_delete_organization(
        client: TestClient,
        db: Session,
        superuser_token_headers: Dict[str, str]
) -> None:

    organization_to_delete = crud.get_by_name(db, "TestOrg")

    r = client.delete(
        f'{settings.API_V1_STR}/organizations/{organization_to_delete.id}',
        headers=superuser_token_headers
    )

    assert r.status_code == 204
