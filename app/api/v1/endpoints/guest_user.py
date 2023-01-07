from typing import Any
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request

from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.dependencies import get_db
from app.utils import sms_sender as sms
from app.crud import crud_basic_user as crud
from app.core.config import settings
from app import schemas
from app.crud import crud_location as location_crud
from app.crud import crud_zones as zone_crud
from app.utils import geocoding


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post('/request-otp')
@limiter.limit('{}/hour'.format(settings.OTP_HOUR_RATE_LIMIT))
async def request_otp_code(
        request: Request,
        phone_number: str,
        db: Session = Depends(get_db)
) -> Any:

    if not settings.EMAILS_ENABLED:
        raise HTTPException(
            status_code=400,
            detail="Cannot send an otp code, please try again later."
        )

    guest_user = crud.get_or_create(db, phone_number)

    otp_status = sms.send_otp(
        phone_number=phone_number,
        code_length=6,
        validity_period=settings.OTP_EXPIRE_MINUTES,
        brand_name=settings.PROJECT_NAME,
        source="Location request",
        language="en-US"
    )
    if not otp_status or otp_status["StatusCode"] != 200:
        raise HTTPException(
            status_code=400,
            detail="Cannot send an otp code, please try again later."
        )

    updated_guest_user = crud.new_otp_request(
        db,
        guest_user.id
    )

    return {
        "status": "success",
        "expiration_minutes": settings.OTP_EXPIRE_MINUTES,
        "expires_at": (datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)).strftime('%Y-%m-%dT%H:%M:%SZ')
    }


@router.post('/request-location')
async def request_location_info_with_otp(
        request: Request,
        location_request: schemas.LocationRequestOtp,
        db: Session = Depends(get_db)
) -> Any:

    if not settings.EMAILS_ENABLED:
        raise HTTPException(
            status_code=400,
            detail="Cannot verify otp codes at the moment, please try again later."
        )

    guest_user = crud.get_or_create(db, location_request.phone_number)

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

    existing_location = location_crud.get_location_by_coordinates(
        db,
        location_request.lat,
        location_request.lng
    )

    if existing_location:
        raise HTTPException(
            status_code=400,
            detail="Review request for this location was already sent."
        )

    address = geocoding.reverse(
        location_request.lat,
        location_request.lng
    )

    if not address:
        raise HTTPException(
            status_code=400,
            detail="Cannot get the address of this location, please check your coordinates."
        )

    restricted_intersection = zone_crud.check_new_point_intersections(
        db,
        location_request.lng,
        location_request.lat
    )

    if restricted_intersection:
        raise HTTPException(
            status_code=403,
            detail="Locations in this area are restricted."
        )

    location_to_review = location_crud.create_location_review_request(
        db,
        address=address,
        lat=location_request.lat,
        lng=location_request.lng,
        requested_by=guest_user.id
    )

    if not location_to_review:
        raise HTTPException(
            status_code=500,
            detail="Encountered an unexpected error, please try again later."
        )

    return location_to_review.to_json()

