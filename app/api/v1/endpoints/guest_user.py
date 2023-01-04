from typing import Any
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.utils import sms_sender as sms
from app.crud import crud_basic_user as crud
from app.core.config import settings
from app import schemas


router = APIRouter()


@router.post('/request-otp')
async def request_otp_code(
        phone_number: str,
        db: Session = Depends(get_db)
) -> Any:
    client = crud.get_or_create(db, phone_number)

    otp_status = sms.send_otp(phone_number, 6, 15, settings.PROJECT_NAME, "Location request", "en-US")
    if not otp_status or otp_status["StatusCode"] != 200:
        raise HTTPException(
            status_code=400,
            detail="Cannot send an otp code, please try again later."
        )

    return {
        "status": "success",
        "expiration_minutes": 15,
        "expires_at": (datetime.utcnow() + timedelta(minutes=15)).strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    # return JSONResponse(status_code=status.HTTP_200_OK, content="Code sent. Please check your phone.")


@router.post('/request-location')
async def request_location_info_with_otp(
        location_request: schemas.LocationRequestOtp,
        db: Session = Depends(get_db)
) -> Any:

    otp_verification = sms.verify_otp(
        location_request.phone_number,
        location_request.otp,
        settings.PROJECT_NAME,
        "Location request"
    )

    if not otp_verification or not otp_verification["Valid"]:
        raise HTTPException(
            status_code=400,
            detail="Provided otp is not valid or expired"
        )

    pass

