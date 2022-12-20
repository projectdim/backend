from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Security, status, Response

from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_active_user
from app import schemas, models
from app.utils import geocoding
from app.crud import crud_zones as crud


router = APIRouter()


@router.post('/restrict')
async def restrict_zone(
        zone: schemas.ZoneBase,
        db: Session = Depends(get_db),
        current_user: models.User = Security(get_current_active_user,
                                             scopes=['zones:restrict'])
) -> Any:

    existing_zone = crud.get_zone_by_verbose_name(db, zone.value)
    if existing_zone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Such zone already exists"
        )

    geom = geocoding.get_bounding_box_by_region_name(zone.value)
    restricted_zone = crud.add_restricted_zone(db, zone.zone_type, zone.value, str(geom))

    return restricted_zone


@router.delete('/allow')
async def allow_zone(
        zone_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Security(get_current_active_user,
                                             scopes=['zones:unrestrict'])
) -> Any:

    result = crud.allow_zone(db, zone_id)
    if not result:
        raise HTTPException(status_code=400, detail="No such zone.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/zones')
async def get_restricted_zones(
        db: Session = Depends(get_db),
        current_user: models.User = Security(get_current_active_user,
                                             scopes=['zones:get'])
) -> Any:

    zones = crud.get_all_restricted_zones(db)
    return zones
