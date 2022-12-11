from typing import Dict

from fastapi.testclient import TestClient

from sqlalchemy.orm import Session

from app.crud import crud_geospatial as geo_crud
from app.crud import crud_location as location_crud
from app.core.config import settings
from app.utils.populate_db import populate_reports


def test_request_location_info(client: TestClient, db: Session) -> None:

    # A sample location in Vinnitsya
    payload = {
        "address": "вул. Стеценко, 64",
        "lat": 49.24003079548452,
        "lng": 28.480316724096923,
        "index": 21000,
        "city": "Вінниця",
        "country": "Україна"
    }

    r = client.post(f"{settings.API_V1_STR}/locations/request-info", json=payload)
    assert 200 <= r.status_code < 300

    requested_location = r.json()
    location = location_crud.get_location_by_id(db, location_id=requested_location['id'])
    assert location.status == 1
    assert location.address == requested_location["address"]
    geospatial_record = geo_crud.search_index_by_location_id(db, location_id=location.id)
    assert geospatial_record
    assert geospatial_record.geohash


def test_get_location_by_address(client: TestClient, db: Session) -> None:

    r = client.get(f'{settings.API_V1_STR}/locations/search-by-name?address=вул. Стеценко, 64')
    assert 200 <= r.status_code < 300

    requested_location = r.json()
    assert requested_location.address == "вул. Стеценко, 64"


def test_get_location_by_coords(client: TestClient, db: Session) -> None:

    # Querying the previously created location
    r = client.get(f"{settings.API_V1_STR}/locations/search?lat=49.24003079548452&lng=28.480316724096923")
    assert 200 <= r.status_code < 300

    requested_location = r.json()
    assert requested_location


def test_pending_location_count(client: TestClient, db: Session, superuser_token_headers: Dict[str, str]) -> None:

    r = client.get(f"{settings.API_V1_STR}/locations/pending-count", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300

    location_count = r.json()
    assert "count" in location_count


def test_get_pending_locations(client: TestClient, db: Session, superuser_token_headers: Dict[str, str]) -> None:

    # TODO testing with the user geolocation?
    r = client.get(f"{settings.API_V1_STR}/locations/location-requests", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300


def test_assign_location(
        client: TestClient,
        db: Session,
        superuser_token_headers: Dict[str, str],
        location_id: int,
        superuser_id: int
) -> None:

    r = client.get(f"{settings.API_V1_STR}/locations/location-requests", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    pending_locations = r.json()
    assert pending_locations

    r = client.put(f"{settings.API_V1_STR}/locations/assign-location?location_id={location_id}", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    assigned_location = r.json()

    assert assigned_location["reported_by"] == superuser_id
    assert assigned_location["status"] == 1


def test_get_assigned_locations(
        client: TestClient,
        db: Session,
        superuser_token_headers: Dict[str, str],
        superuser_id: int
) -> None:

    r = client.get(f"{settings.API_V1_STR}/locations/assigned-locations", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    assigned_locations = r.json()

    # Checking that all the received locations are actually assigned to the same user
    for location in assigned_locations:
        assert location["reported_by"] == superuser_id
        assert location["status"] == 1


def test_remove_assigned_location(
        client: TestClient,
        db: Session,
        superuser_token_headers: Dict[str, str],
        location_id: int
) -> None:

    r = client.get(f"{settings.API_V1_STR}/locations/assigned-locations", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    assigned_locations = r.json()
    assert assigned_locations

    r = client.put(f"{settings.API_V1_STR}/locations/remove-assignment?location_id={location_id}", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    pending_location = r.json()
    assert pending_location['reported_by'] is None
    assert pending_location["report_expires"] is None


def test_submit_location_report(
        client: TestClient,
        db: Session,
        superuser_token_headers: Dict[str, str],
        location_id: int,
        superuser_id: int
) -> None:

    r = client.get(f"{settings.API_V1_STR}/locations/location-requests", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    pending_locations = r.json()
    assert pending_locations

    random_reports = populate_reports()
    random_reports["location_id"] = location_id

    r = client.put(f"{settings.API_V1_STR}/locations/submit-report", json=random_reports, headers=superuser_token_headers)
    assert 200 <= r.status_code < 300

    reported_location = r.json()
    assert reported_location
    assert reported_location["status"] == 3
    assert reported_location["reports"]
    assert reported_location["reported_by"] == superuser_id
    assert reported_location["report_expires"] is None


def test_get_location_info(client: TestClient, db: Session, location_id: int) -> None:

    locations = location_crud.get_all_locations(db)

    r = client.get(f'{settings.API_V1_STR}/locations/location-info?location_id={location_id}')
    assert 200 <= r.status_code < 300
    requested_location = r.json()

    assert requested_location
    assert requested_location["reports"]
    assert requested_location["status"] == 3


def test_get_location_changelogs(client: TestClient, db: Session, location_id: int) -> None:
    locations = location_crud.get_all_locations(db)

    r = client.get(f'{settings.API_V1_STR}/locations/changelogs?location_id={location_id}')
    assert 200 <= r.status_code < 300
    location_changelogs = r.json()

    assert location_changelogs
    for log in location_changelogs:
        assert log["new_flags"]


def test_remove_location(client: TestClient, db: Session, superuser_token_headers: Dict[str, str], location_id: int) -> None:
    locations = location_crud.get_all_locations(db)

    r = client.delete(f'{settings.API_V1_STR}/locations/remove-location?location_id={location_id}', headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    # deleted_location = r.json()
    #
    # location_in_db = location_crud.get_location_by_id(db, location_id=location_id)
    # print(location_in_db)
    # assert location_in_db is None
