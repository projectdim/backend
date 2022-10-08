from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User, role_permissions
from app.schemas.user import UserCreate, UserBase


def get_by_email(db: Session, *, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get(db: Session, *, user_id: int) -> Optional[User]:
    return db.query(User).get(user_id)


def create(db: Session, *, obj_in: UserCreate) -> User:
    db_obj = User(
        email=obj_in.email,
        username=obj_in.username,
        hashed_password=get_password_hash(obj_in.password),
        full_name=obj_in.full_name,
        role="aid_worker",
        permissions=role_permissions["aid_worker"]
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_info(db: Session, *, obj_in: UserBase, user_email: str) -> User:
    user = get(db, user_email=user_email)

    user.email = obj_in.email
    user.full_name = obj_in.full_name
    user.username = obj_in.username

    db.commit()
    db.refresh(user)
    return user


def update_password(db: Session,
                    user_email: str,
                    old_password: str,
                    new_password: str) -> User:

    user = authenticate(db, email=user_email, password=old_password)
    if not user:
        return None

    user.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, *, email: str, password: str) -> Optional[User]:
    user = get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
