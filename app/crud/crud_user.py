from typing import Optional
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User, role_permissions
from app.schemas.user import UserCreate, UserBase, UserInvite
from app.core.config import settings
from app.crud.crud_roles import get_role_by_name


def get_by_email(db: Session, *, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get(db: Session, *, user_id: int) -> Optional[User]:
    return db.query(User).get(user_id)


def create(db: Session, *, obj_in: UserCreate, role: str) -> Optional[User]:

    user_role = get_role_by_name(db, role)

    if not user_role:
        return None

    db_obj = User(
        email=obj_in.email,
        username=obj_in.username,
        hashed_password=get_password_hash(obj_in.password),
        full_name=obj_in.full_name,
        role=user_role.verbose_name,
        organization=obj_in.organization,
        permissions=user_role.permissions,
        email_confirmed=True,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_invite(db: Session, *, obj_in: UserInvite) -> Optional[User]:

    user_role = get_role_by_name(db, "aid_worker")
    if not user_role:
        return None

    # TODO CHECK IF ORGANIZATION EXISTS

    db_obj = User(
        email=obj_in.email,
        organization=obj_in.organization,
        is_active=False,
        role=user_role.verbose_name,
        permissions=user_role.permissions,
        registration_token=create_access_token(subject=obj_in.email, scopes=['users:confirm']),
        registration_token_expires=datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def confirm_registration(db: Session, *, access_token: str, obj_in: UserCreate) -> Optional[User]:
    invited_user = db.query(User).filter(User.registration_token == access_token).first()

    # TODO CHECK IF TOKEN NOT EXPIRED
    if not invited_user:
        return None

    invited_user.registration_token = None
    invited_user.registration_token_expires = None
    invited_user.full_name = obj_in.full_name
    invited_user.username = obj_in.username
    invited_user.hashed_password = get_password_hash(obj_in.password)
    invited_user.is_active = True
    invited_user.email_confirmed = True

    db.commit()
    db.refresh(invited_user)
    return invited_user


def update_info(db: Session, *, obj_in: UserBase, user_email: str) -> User:
    user = get_by_email(db, email=user_email)

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


def delete_user(db: Session, user_id: int) -> Optional[User]:
    user = get(db, user_id=user_id)
    if not user:
        return None

    db.delete(user)
    db.commit()
    return get(db, user_id=user_id)
