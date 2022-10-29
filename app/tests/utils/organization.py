from sqlalchemy.orm import Session

from app.crud import crud_organizations as crud


def get_master_organization(db: Session) -> int:
    return crud.get_by_name(db, "DIM").id
