from typing import Any
import json

from fastapi import APIRouter, Depends, HTTPException, Body, Security

from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_active_user
from app import schemas, models
from app.crud import crud_location as crud
from app.crud import crud_changelogs as logs_crud


router = APIRouter()


@router.post('/create')
async def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)) -> Any:

    # existing_location = crud.get_location_by_index(db, location.index)
    #
    # if existing_location:
    #     raise HTTPException(status_code=400, detail="Location already exists.")

    new_location = crud.create_location(db, obj_in=location)

    if not new_location:
        raise HTTPException(status_code=400, detail="Cannot create a location")

    return new_location.to_json()


@router.get('/search')
async def get_location(lat: float, lng: float, db: Session = Depends(get_db)) -> Any:

    location = crud.get_location_by_coordinates(db, lat, lng)

    if not location:
        raise HTTPException(status_code=400, detail="Not found")

    return location.to_json()


@router.post('/cord_search')
async def get_locations_by_coordinates(coordinates: schemas.LocationSearch, db: Session = Depends(get_db)) -> Any:

    locations = crud.get_locations_in_range(db, coordinates.lat, coordinates.lng)

    return [location.to_json() for location in locations]


@router.get('/changelogs')
async def get_location_changelogs(location_id: int, db: Session = Depends(get_db)) -> Any:

    logs = logs_crud.get_changelogs(db, location_id)

    return logs


@router.post('/request-info')
async def request_location_review(location: schemas.LocationCreate, db: Session = Depends(get_db)) -> Any:

    existing_location = crud.get_location_by_coordinates(db, location.lat, location.lng)

    if existing_location:
        raise HTTPException(status_code=400, detail="Review request for this location was already sent")

    location_to_review = crud.create_location_review_request(db, obj_in=location)

    if not location_to_review:
        raise HTTPException(status_code=500, detail="Cannot connect to the database, please try again")

    return location_to_review.to_json()


@router.get('/location-requests',)
async def get_requested_locations(page: int = 1,
                                  limit: int = 20,
                                  db: Session = Depends(get_db),
                                  current_user: models.User = Security(get_current_active_user,
                                                                       scopes=['locations:view'])) -> Any:

    locations = crud.get_locations_awaiting_reports(db, limit, page - 1)

    return [location.to_json() for location in locations]
