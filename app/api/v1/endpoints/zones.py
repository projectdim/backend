from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Security, status, Response

from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_active_user
from app import schemas, models


router = APIRouter()


@router.post('/restrict')
async def restrict_zone(
        zone: schemas.ZoneBase,
        db: Session = Depends(get_db),
        current_user: models.User = Security(get_current_active_user,
                                             scopes=['zones:restrict'])
):
    pass


@router.delete('/unrestrict')
async def unrestrict_zone(
        zone_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Security(get_current_active_user,
                                             scopes=['zones:unrestrict'])
):
    pass


@router.get('/zones')
async def get_restricted_zones(
        zone_type: int,
        db: Session = Depends(get_db),
        current_user: models.User = Security(get_current_active_user,
                                             scopes=['zones:get'])
):
    pass
