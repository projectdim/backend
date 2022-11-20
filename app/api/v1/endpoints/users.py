from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Security, status, Response

from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_active_user
from app import schemas, models
from app.crud import crud_user as crud

from app.core.config import settings


router = APIRouter()


@router.post('/register', response_model=schemas.UserOut)
async def register_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db),
        current_active_user: models.User = Security(get_current_active_user, scopes=['users:create'])
) -> Any:

    existing_user = crud.get_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User exists")

    new_user = crud.create(db, obj_in=user, role="aid_worker")

    if not new_user:
        raise HTTPException(status_code=500, detail="Cannot connect to db, please try again later")

    # TODO EMAIL CONFIRMATION

    return new_user


@router.post('/invite', response_model=schemas.UserOut)
async def generate_invite_link(
        user: schemas.UserInvite,
        db: Session = Depends(get_db),
        current_active_user: models.User = Security(get_current_active_user, scopes=['users:create'])
) -> Any:

    # if user.email == settings.TEST_USER_EMAIL:
    #     raise HTTPException(status_code=400, detail='This email is reserved.')

    existing_user = crud.get_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User exists")

    new_user = crud.create_invite(db, obj_in=user)

    if not new_user:
        raise HTTPException(status_code=500, detail="Cannot connect to db, please try again later")

    # TODO EMAIL MODULE

    return new_user


@router.post('/confirm-registration', response_model=schemas.UserOut)
async def confirm_user_registration(
        access_token: str,
        user: schemas.UserCreate,
        db: Session = Depends(get_db)
) -> Any:

    new_user = crud.confirm_registration(db, access_token=access_token, obj_in=user)

    if not new_user:
        raise HTTPException(status_code=400, detail="Cannot create a new user. Please ask for invite link once more")

    return new_user


@router.get('/me', response_model=schemas.UserOut)
async def get_me(
        current_user: models.User = Security(get_current_active_user, scopes=['users:me'])
) -> Any:

    return current_user


@router.put('/info', response_model=schemas.UserOut)
async def patch_user_info(
        updated_info: schemas.UserBase,
        current_user: models.User = Security(get_current_active_user, scopes=['users:edit']),
        db: Session = Depends(get_db)
) -> Any:

    updated_user = crud.update_info(db, obj_in=updated_info, user_email=current_user.email)

    return updated_user


@router.put('/password', response_model=schemas.UserOut)
async def change_user_password(
        updated_info: schemas.UserPasswordUpdate,
        current_user: models.User = Security(get_current_active_user, scopes=['users:edit']),
        db: Session = Depends(get_db)
) -> Any:

    updated_user = crud.update_password(db,
                                        user_email=current_user.email,
                                        old_password=updated_info.old_password,
                                        new_password=updated_info.new_password)
    if not updated_user:
        raise HTTPException(status_code=400, detail='The provided password was incorrect.')

    return updated_user


@router.put('/change-role', response_model=schemas.UserOut)
async def change_user_role(
        user_id: int,
        role: str,
        current_user: models.User = Security(get_current_active_user, scopes=['users:roles']),
        db: Session = Depends(get_db)
) -> Any:

    updated_user = crud.change_role(db, user_id=user_id, role=role)

    if not updated_user:
        raise HTTPException(status_code=400, detail='Cannot update user')

    return updated_user


# TODO do we need this? Is the edit permission right for such operation (reserved route for tests)
@router.delete('/delete-me')
async def delete_me(
        current_user: models.User = Security(get_current_active_user, scopes=['users:edit']),
        db: Session = Depends(get_db)
) -> Any:

    deleted_user = crud.delete_user(db, current_user.id)

    if deleted_user:
        raise HTTPException(status_code=400, detail="Cannot perform such action")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# TODO user change organization route
# TODO user change role route

