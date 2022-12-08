from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Security, status, Response

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
                                                                            scopes=["organizations:view"])) -> Any:
    return crud.get_organizations_list(db, limit=limit, skip=page - 1)


@router.get('/search', response_model=List[schemas.OrganizationOut])
async def search_organizations_by_name(
        query: str,
        db: Session = Depends(get_db),
        current_active_user: models.User = Security(get_current_active_user,
                                                    scopes=["organizations:view"])
) -> Any:
    organizations = crud.get_by_substr(db, query.lower())
    if not organizations:
        return []

    return organizations


@router.get('/{organization_id}', response_model=schemas.OrganizationOut)
async def get_organization_by_id(organization_id: int, db: Session = Depends(get_db),
                                 current_active_user: models.User = Security(get_current_active_user,
                                                                             scopes=['organizations:view'])) -> Any:
    organization = crud.get_by_id(db, organization_id=organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Not found")

    return organization


@router.put('/{organization_id}/edit', response_model=schemas.OrganizationOut)
async def edit_organization_data(
        organization_id: int,
        data: schemas.OrganizationBase,
        db: Session = Depends(get_db),
        current_active_user: models.User = Security(get_current_active_user, scopes=['organizations:edit'])
) -> Any:

    updated_organization = crud.edit_organization(db,
                                                  organization_id=organization_id,
                                                  obj_in=data)
    if not updated_organization:
        raise HTTPException(status_code=404, detail="Not found")

    return updated_organization


@router.put('/{organization_id}/invite', response_model=schemas.OrganizationOut)
async def invite_organization_members(
        organization_id: int,
        users: schemas.OrganizationUserInvite,
        db: Session = Depends(get_db),
        current_active_user: models.User = Security(get_current_active_user, scopes=['organizations:edit'])
) -> Any:
    organization = crud.get_by_id(db, organization_id=organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Not found")

    updated_organization = crud.add_members(db, organization_id=organization_id, user_emails=users.emails)

    return updated_organization


@router.put('/{organization_id}/remove', response_model=schemas.OrganizationOut)
async def remove_organization_member(
        organization_id: int,
        user_id: int,
        db: Session = Depends(get_db),
        current_active_user: models.User = Security(get_current_active_user, scopes=['organizations:edit'])
) -> Any:
    organization = crud.get_by_id(db, organization_id=organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Not found")

    updated_organization = crud.remove_members(db, organization_id=organization_id, user_id=user_id)
    if not updated_organization:
        raise HTTPException(status_code=400, detail="This user does not belong to such organization")

    return updated_organization


@router.delete('/{organization_id}')
async def delete_organization(
        organization_id: int,
        db: Session = Depends(get_db),
        current_active_user: models.User = Security(get_current_active_user, scopes=['organizations:delete'])
) -> Any:
    organization = crud.get_by_id(db, organization_id=organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Not found")

    removed_organization = crud.delete_organization(db, organization_id=organization_id)
    if removed_organization:
        raise HTTPException(status_code=400, detail="Cannot perform such action")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
