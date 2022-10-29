from sqlalchemy.orm import Session

from app.crud import crud_user as crud
from app.crud import crud_roles as role_crud
from app.crud import crud_organizations as org_crud
from app.schemas import UserCreate, UserRole, OrganizationBase
from app.models import User
from app.core.config import settings


def init_db(db: Session) -> User:
    # TODO CREATE PERMISSION PRESETS INSTEAD OF EXPLICIT DECLARATION
    # initializing base roles
    role = role_crud.get_role_by_name(db, "platform_administrator")
    if not role:
        role_crud.create_role(db, obj_in=UserRole(
            verbose_name="platform_administrator",
            permissions=[
                "locations:view",
                "locations:edit",
                "locations:delete",
                "users:create",
                "users:me",
                "users:edit",
                "organizations:view",
                "organizations:create",
                "organizations:edit",
                "organizations:delete"
            ]))

    aid_worker = role_crud.get_role_by_name(db, "aid worker")
    if not aid_worker:
        role_crud.create_role(db, obj_in=UserRole(
            verbose_name="aid_worker",
            permissions=["locations:view",
                         "locations:edit",
                         "users:me",
                         "users:edit"
                         ]))

    # creating the "DIM" organization
    organization = org_crud.get_by_name(db, "DIM")
    if not organization:
        organization = org_crud.create(db, obj_in=OrganizationBase(name="DIM"))

    # creating first superuser
    user = crud.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        new_user = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            organization=organization.id
        )
        user = crud.create(db, obj_in=new_user, role="platform_administrator")

    return user
