from sqlalchemy.orm import Session

from app.models import Location

from app.crud import crud_location as crud


def get_location(db: Session) -> Location:

    locations = crud.get_all_locations(db)

    return locations[0]
