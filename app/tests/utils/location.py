from typing import Dict

from sqlalchemy.orm import Session

from fastapi.testclient import TestClient

from app.models import Location
from app.crud import crud_location as crud
from app.core.config import settings


def get_location(db: Session) -> Location:

    locations = crud.get_all_locations(db)

    return locations[0]


def create_sample_location_request(client: TestClient) -> Dict[str, str]:

    payload = {
        "lat": 49.24003079548452,
        "lng": 28.480316724096923
    }

    r = client.post(f"{settings.API_V1_STR}/locations/request-info", json=payload)
    return r.json()

