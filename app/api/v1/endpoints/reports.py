from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_active_user
from app.crud import crud_reports as crud


router = APIRouter()


@router.post('/create')
async def create_report():
    pass
