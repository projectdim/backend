from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Security

from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_active_user
from app import schemas, models
from app.crud import crud_organizations as crud


router = APIRouter()


@router.post('/create', response_model=schemas.OrganizationOut)
async def create_organization(organization: schemas.OrganizationBase,
                              db: Session = Depends(get_db),
                              current_active_user: models.User = Security(get_current_active_user,
                                                                          scopes=["organizations:create"])) -> Any:

    existing_organization = crud.get_by_name(db, organization.name)

    if existing_organization:
        raise HTTPException(status_code=400, detail="Organization exists")

    new_organization = crud.create(db, obj_in=organization)

    if not new_organization:
        raise HTTPException(status_code=500, detail="Cannot connect to the database. Please try again later")

    return new_organization


@router.get('/all', response_model=List[schemas.OrganizationOut])
async def get_organization_list(page: int = 1, limit: int = 20,
                                db: Session = Depends(get_db),
                                current_active_user: models.User = Security(get_current_active_user,
                                                                            scopes=["organizations:view"])):

    return crud.get_organizations_list(db, limit=limit, skip=page - 1)
