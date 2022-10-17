from sqlalchemy.orm import Session

from app.crud import crud_user as crud
from app.schemas import UserCreate
from app.models import User
from app.core.config import settings


def init_db(db: Session) -> User:

    user = crud.get_by_email(db, email=settings.FIRST_SUPERUSER)

    if not user:
        new_user = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        user = crud.create(db, obj_in=new_user, role="platform_administrator")

    return user
