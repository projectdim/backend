import random
import datetime
from typing import List, Any

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.utils.time_generator import random_date
from app.models.changelog import ChangeLog
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate


def create_location(db: Session, *, obj_in: LocationCreate) -> Location:

    reports = {
        "buildingCondition": "Неушкоджена",
        "electricity": "Переривчаста",
        "carEntrance": random.choice(["Доступне", "Недоступне"]),
        "water": random.choice(['Стабільна', "Нестабільна"]),
        "fuelStation": "відчинено",
        "fuelStationDistance": random.uniform(0.1, 9.8),
        "hospital": random.choice(['зачинено', 'відчинено']),
        "hospitalDistance": random.uniform(0.1, 9.9)
    }

    try:
        db_obj = Location(
            address=obj_in.address,
            index=obj_in.index,
            lat=obj_in.lat,
            lng=obj_in.lng,
            country=obj_in.country,
            city=obj_in.city,
            reports=reports
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return_obj = db.query(Location).filter(Location.id == db_obj.id).first()
        random_time = datetime.datetime.strptime(random_date("9/1/2022 1:30 PM", "9/18/2022 4:50 PM", random.random()),
                                                 '%m/%d/%Y %I:%M %p')

        db_changelog = ChangeLog(
            created_at=random_time,
            location_id=return_obj.id,
            action_type=1,
            old_flags={"buildingCondition": "Пошкоджена"},
            new_flags={"buildingCondition": "Неушкоджена"}
        )
        db.add(db_changelog)
        db.commit()
        db.refresh(db_changelog)

        random_time = datetime.datetime.strptime(random_date("9/1/2022 1:30 PM", "9/18/2022 4:50 PM", random.random()),
                                                 '%m/%d/%Y %I:%M %p')

        db_changelog = ChangeLog(
            created_at=random_time,
            location_id=return_obj.id,
            action_type=1,
            old_flags={"electricity": "Переривчаста", "fuelStation": "зачинено"},
            new_flags={"electricity": "Стабільна", "fuelStation": "відчинено"}
        )
        db.add(db_changelog)
        db.commit()
        db.refresh(db_changelog)

        random_time = datetime.datetime.strptime(random_date("9/1/2022 1:30 PM", "9/18/2022 4:50 PM", random.random()),
                                                 '%m/%d/%Y %I:%M %p')

        db_changelog = ChangeLog(
            created_at=random_time,
            location_id=return_obj.id,
            action_type=2,
            media_url="http://static.prsa.pl/images/22f26b47-af71-4daa-a669-07f10bc23810.jpg"
        )
        db.add(db_changelog)
        db.commit()
        db.refresh(db_changelog)

        return return_obj

    except Exception as e:
        print(e)
        return None


def create_location_review_request(db: Session, *, obj_in: LocationCreate) -> Location:

    try:
        db_obj = Location(
            address=obj_in.address,
            index=obj_in.index,
            lat=obj_in.lat,
            lng=obj_in.lng,
            status=1,
            country=obj_in.country,
            city=obj_in.city,
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    except Exception as e:
        print(e)
        return None


def get_location_by_index(db: Session, index: int) -> Location:
    return db.query(Location).filter(Location.index == index).first()


def get_location_by_coordinates(db: Session, lat: float, lng: float) -> Location:
    return db.query(Location).filter(Location.lat == lat, Location.lng == lng).first()


def get_locations_in_range(db: Session, lat: dict, lng: dict) -> List[Location]:
    return db.query(Location)\
        .filter(Location.lat.between(lat["lo"], lat["hi"]),
                Location.lng.between(lng["lo"], lng["hi"]),
                Location.status == 3).all()


def get_locations_awaiting_reports(db: Session, limit: int = 20, skip: int = 0) -> List[Location]:
    return db.query(Location).filter(Location.status == 1)\
        .order_by(desc(Location.created_at))\
        .limit(limit)\
        .offset(skip * limit)
