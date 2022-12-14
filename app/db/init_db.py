from sqlalchemy.orm import Session

from app.crud import crud_user as crud
from app.crud import crud_roles as role_crud
from app.crud import crud_organizations as org_crud
from app.schemas import UserCreate, UserRole, OrganizationBase
from app.models import User
from app.core.config import settings
from app.models.roles import presets as role_presets


def init_db(db: Session) -> User:
    # initializing base roles
    role = role_crud.get_role_by_name(db, "platform_administrator")
    if not role:
        role_crud.create_role(
            db,
            obj_in=UserRole(
                verbose_name="platform_administrator",
                permissions=role_presets["platform_administrator"]
            )
        )
    if role:
        if role.permissions != role_presets["platform_administrator"]:
            role_crud.update_permissions(db, role_id=role.id, permissions=role_presets["platform_administrator"])

    aid_worker = role_crud.get_role_by_name(db, "aid_worker")
    if not aid_worker:
        role_crud.create_role(
            db,
            obj_in=UserRole(
                verbose_name="aid_worker",
                permissions=role_presets['aid_worker']
            )
        )
    if role:
        if aid_worker.permissions != role_presets['aid_worker']:
            role_crud.update_permissions(db, role_id=aid_worker.id, permissions=role_presets["aid_worker"])

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
