from typing import Optional
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from app.models.guest_user import GuestUser


def create(db: Session, *, phone_number: str) -> GuestUser:

    db_obj = GuestUser(
        phone_number=phone_number
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_by_phone_number(db: Session, phone_number: str) -> Optional[GuestUser]:
    return db.query(GuestUser).filter(GuestUser.phone_number == phone_number).first()


def get_or_create(db: Session, phone_number: str) -> GuestUser:
    user = get_by_phone_number(db, phone_number=phone_number)
    if not user:
        user = create(db, phone_number=phone_number)
    return user


def new_otp_request(
        db: Session,
        user_id: int
) -> GuestUser:

    guest_user = db.query(GuestUser).get(user_id)

    guest_user.last_request = datetime.now()
    guest_user.total_otp_requests = 1 if not guest_user.total_otp_requests else guest_user.total_otp_requests + 1

    db.commit()
    db.refresh(guest_user)

    return guest_user

