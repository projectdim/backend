from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Security, status, Response

from sqlalchemy.orm import Session

from app import models, schemas
from app.api.dependencies import get_current_active_user, get_db
from app.crud import crud_roles as crud

router = APIRouter()


@router.get('/all', response_model=List[schemas.UserRole])
async def get_all_roles(
        current_active_user: models.User = Security(get_current_active_user,
                                                    scopes=['roles:read']),
        db: Session = Depends(get_db)
) -> Any:

    roles = crud.get_all_roles(db)
    return roles
