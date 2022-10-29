from typing import Generator, Dict

import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.db.session import SessionLocal
from app.tests.utils.user import user_authentication_headers, get_superuser_token_headers, get_superuser_id
from app.tests.utils.location import get_location
from app.tests.utils.organization import get_master_organization
from app.core.config import settings


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def aid_worker_token_headers(client: TestClient) -> Dict[str, str]:
    return user_authentication_headers(
        client=client, email=settings.TEST_USER_EMAIL, password=settings.TEST_USER_PASSWORD
    )


@pytest.fixture(scope="module")
def location_id(db: Session) -> int:
    return get_location(db).id


@pytest.fixture(scope="module")
def superuser_id(db: Session) -> int:
    return get_superuser_id(db)


@pytest.fixture(scope="module")
def master_organization_id(db: Session) -> int:
    return get_master_organization(db)

