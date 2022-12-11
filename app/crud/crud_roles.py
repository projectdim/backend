from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import update

from app.models.roles import Role
from app.models.user import User
from app import schemas


def create_role(db: Session, *, obj_in: schemas.UserRole) -> Optional[Role]:

    existing_role = get_role_by_name(db, obj_in.verbose_name)

    if existing_role:
        return None

    db_obj = Role(
        verbose_name=obj_in.verbose_name,
        permissions=obj_in.permissions
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_all_roles(db: Session) -> List[Role]:
    return db.query(Role).all()


def get_role_by_name(db: Session, role_name: str) -> Optional[Role]:
    return db.query(Role).filter(Role.verbose_name == role_name).first()


def update_permissions(db: Session, role_id: int, permissions: list) -> Optional[Role]:
    role = db.query(Role).get(role_id)
    role.permissions = permissions
    db.commit()
    db.refresh(role)

    users = db.query(User).filter(User.role == role.verbose_name).update({User.permissions: permissions})
    db.commit()
    return role

