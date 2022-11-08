from typing import Optional, List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.models.user import User
from app.schemas.organization import OrganizationBase, OrganizationUserInvite


def create(db: Session, *, obj_in: OrganizationBase) -> Organization:

    db_obj = Organization(
        name=obj_in.name,
        website=obj_in.website,
        description=obj_in.description
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_by_id(db: Session, organization_id: int) -> Optional[Organization]:
    return db.query(Organization).get(organization_id)


def get_by_name(db: Session, name: str) -> Optional[Organization]:
    return db.query(Organization).filter(Organization.name == name).first()


def get_by_substr(db: Session, name: str) -> List[Organization]:
    return db.query(Organization).filter(Organization.name.startswith(name)).all()


def get_organizations_list(db: Session, limit: int = 20, skip: int = 0) -> List[Organization]:
    return db.query(Organization).order_by(desc(Organization.created_at))\
        .limit(limit)\
        .offset(skip * limit).all()


def edit_organization(db: Session, organization_id: int, obj_in: OrganizationBase) -> Optional[Organization]:

    organization = get_by_id(db, organization_id=organization_id)
    if not organization:
        return None

    # convert the request to dict to iterate over its fields
    data_to_update = obj_in.dict(exclude_unset=True)
    for field in data_to_update:
        # updated the organization with no explicit field declaration
        setattr(organization, field, data_to_update[field])

    db.commit()
    db.refresh(organization)
    return organization


def add_members(db: Session, organization_id: int, user_emails: List[str]) -> Organization:

    # TODO refactor this!

    for user in user_emails:
        db_user = db.query(User).filter(
            User.email == user,
            User.email_confirmed == True,
            User.is_active == True
        ).first()
        if not db_user:
            continue

        db_user.organization = organization_id
        db.commit()
        db.refresh(db_user)

    return get_by_id(db, organization_id=organization_id)


def remove_members(db: Session, organization_id: int, user_id: int) -> Optional[Organization]:

    db_user = db.query(User).get(user_id)
    if not db_user or not db_user.organization:
        return None

    db_user.organization = None
    db.commit()
    db.refresh(db_user)

    return get_by_id(db, organization_id=organization_id)


def delete_organization(db: Session, organization_id: int) -> Optional[Organization]:

    organization = get_by_id(db, organization_id=organization_id)

    db.delete(organization)
    db.commit()

    return get_by_id(db, organization_id=organization_id)
