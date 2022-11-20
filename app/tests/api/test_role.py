from typing import Dict

from fastapi.testclient import TestClient

from sqlalchemy.orm import Session

from app.crud import crud_roles as crud
from app.core.config import settings


# def test_create_role(
#         client: TestClient,
#         db: Session,
#         superuser_token_headers: Dict[str, str]
# ) -> None:
#
#     pass


def get_all_roles(
        client: TestClient,
        db: Session,
        superuser_token_headers: Dict[str, str]
) -> None:

    r = client.get(f'{settings.API_V1_STR}/roles/all', headers=superuser_token_headers)

    assert 200 <= r.status_code < 300
    assert isinstance(r.json(), list)


