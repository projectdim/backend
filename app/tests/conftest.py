from typing import Generator, Dict

import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy_utils import drop_database, database_exists, create_database

from app.main import app
from app.models.location import Location
from app.db.init_db import init_db
from app.api.dependencies import get_db
from app.db.base import Base
from app.db.session import SessionLocal
from app.tests.utils.user import user_authentication_headers, get_superuser_token_headers, get_superuser_id
from app.tests.utils.location import create_sample_location_request, get_location_by_coords
from app.tests.utils.organization import get_master_organization
from app.core.config import settings
from app.tests.utils.db_setup import get_url

SQLALCHEMY_DATABASE_URL = get_url()

if database_exists(SQLALCHEMY_DATABASE_URL):
    drop_database(SQLALCHEMY_DATABASE_URL)

create_database(SQLALCHEMY_DATABASE_URL)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)
init_db(TestingSessionLocal())


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def test_db() -> Generator:
    yield TestingSessionLocal()


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
def sample_location(client: TestClient) -> Dict[str, str]:
    return create_sample_location_request(client=client)


@pytest.fixture(scope="module")
def sample_location_coordinates() -> Dict:
    return {
        "lat": 49.24003079548452,
        "lng": 28.480316724096923
    }


@pytest.fixture(scope="module")
def location(test_db: Session, sample_location_coordinates: Dict) -> Location:
    return get_location_by_coords(test_db, sample_location_coordinates)


@pytest.fixture(scope="module")
def superuser_id(test_db: Session) -> int:
    return get_superuser_id(test_db)


@pytest.fixture(scope="module")
def master_organization_id(test_db: Session) -> int:
    return get_master_organization(test_db)

