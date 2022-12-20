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
