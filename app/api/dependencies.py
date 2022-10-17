from typing import Generator
from datetime import datetime

from fastapi import Depends, HTTPException, status, Security
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi.security import SecurityScopes
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import models, crud, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login/token",
                                       scopes={"me": "Read current user information",
                                               "locations": "Get info about locations"}, )


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db

    finally:
        db.close()


def get_current_user(security_scopes: SecurityScopes,
                     db: Session = Depends(get_db),
                     token: str = Depends(reusable_oauth2)) -> models.User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value}
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenBase(**payload)

    except (jwt.JWTError, ValidationError) as e:
        print(e)
        raise credentials_exception

    user = crud.crud_user.get(db, user_id=token_data.sub)
    if not user:
        raise credentials_exception

    # TODO
    # session = crud.crud_sessions.get_by_access_token(db, user_id=user.id, access_token=token)
    # if not session.is_active or not session:
    #     raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value}
            )

    return user


def get_current_active_user(current_user: models.User = Security(get_current_user, scopes=["users:me"])) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="User is not active")

    return current_user
