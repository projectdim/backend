from typing import Optional, List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.schemas.organization import OrganizationBase


def create(db: Session, *, obj_in: OrganizationBase) -> Organization:

    db_obj = Organization(
        name=obj_in.name,
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_by_id(db: Session, organization_id: int) -> Optional[Organization]:
    return db.query(Organization).get(organization_id)


def get_by_name(db: Session, name: str) -> Optional[Organization]:
    return db.query(Organization).filter(Organization.name == name).first()


def get_organizations_list(db: Session, limit: int = 20, skip: int = 0) -> List[Organization]:
    return db.query(Organization).order_by(desc(Organization.created_at))\
        .limit(limit)\
        .offset(skip * limit)
