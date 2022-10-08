from typing import Any, List
from datetime import timedelta

from fastapi import Depends, HTTPException, APIRouter

from sqlalchemy.orm import Session

from app.crud import crud_sessions as crud
from app.api.dependencies import get_db, get_current_active_user
from app import models, schemas


router = APIRouter()


@router.get('/active', response_model=List[schemas.UserSession])
async def get_active_sessions(current_user: models.User = Depends(get_current_active_user),
                              db: Session = Depends(get_db)):
    sessions = crud.get_user_active_sessions(db, user_id=current_user.id)

    return sessions


@router.post('/revoke', response_model=schemas.UserSession)
async def revoke_user_session(session_id: int, current_user: models.User = Depends(get_current_active_user),
                              db: Session = Depends(get_db)):

    revoked_session = crud.revoke_by_id(db, user_id=current_user.id, session_id=session_id)
    if not revoked_session:
        raise HTTPException(status_code=400, detail="Cannot revoke this session")

    return revoked_session
