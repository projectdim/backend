from typing import Dict

from fastapi.testclient import TestClient

from sqlalchemy.orm import Session

from app.utils.geocoding import get_bounding_box_by_region_name
from app.core.config import settings
from app.crud import crud_zones as crud


def test_restrict_zone(
        client: TestClient,
        db: Session,
        superuser_token_headers: Dict[str, str]
) -> None:

    payload = {
        "zone_type": 1,
        "value": "Crimea"
    }

    r = client.post(f'{settings.API_V1_STR}/zones/restrict', json=payload, headers=superuser_token_headers)

    assert 200 <= r.status_code < 300
    restricted_location = r.json()
    assert restricted_location['bounding_box']
    assert restricted_location['bounding_box'] == str(get_bounding_box_by_region_name('Crimea'))


def test_request_location_in_restricted_zone(
        client: TestClient,
        db: Session
) -> None:

    # sample location coordinates in Crimea
    payload = {
        "lat": 45.37232512282975,
        "lng": 33.94657337107382
    }

    r = client.post(f"{settings.API_V1_STR}/locations/request-info", json=payload)
    assert r.status_code == 403


def test_get_all_restricted_zones(
        client: TestClient,
        db: Session,
        superuser_token_headers: Dict[str, str]
) -> None:

    r = client.get(f'{settings.API_V1_STR}/zones/zones', headers=superuser_token_headers)
    assert 200 <= r.status_code < 300

    zones = r.json()
    assert isinstance(zones, list)
    assert len(zones) > 0


def test_allow_zone(
        client: TestClient,
        db: Session,
        superuser_token_headers: Dict[str, str]
) -> None:

    existing_zone = crud.get_zone_by_verbose_name(db, 'Crimea')
    r = client.delete(
        f'{settings.API_V1_STR}/zones/allow?zone_id={existing_zone.id}',
        headers=superuser_token_headers
    )
    assert r.status_code == 204
