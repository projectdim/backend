import random
import datetime
from typing import List, Any

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.utils.time_generator import random_date
from app.models.changelog import ChangeLog
from app.crud.crud_changelogs import create_changelog
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationReports
from app.utils.populate_db import populate_reports


def create_location(db: Session, *, obj_in: LocationCreate) -> Location:

    try:
        db_obj = Location(
            address=obj_in.address,
            index=obj_in.index,
            lat=obj_in.lat,
            lng=obj_in.lng,
            country=obj_in.country,
            city=obj_in.city,
            reports=populate_reports()
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        for i in range(3):
            submit_location_reports(db, obj_in=LocationReports(**populate_reports()))

        # return_obj = db.query(Location).filter(Location.id == db_obj.id).first()
        # random_time = datetime.datetime.strptime(random_date("9/1/2022 1:30 PM", "9/18/2022 4:50 PM", random.random()),
        #                                          '%m/%d/%Y %I:%M %p')
        #
        # db_changelog = ChangeLog(
        #     created_at=random_time,
        #     location_id=return_obj.id,
        #     action_type=1,
        #     old_flags={"buildingCondition": "Пошкоджена"},
        #     new_flags={"buildingCondition": "Неушкоджена"}
        # )
        # db.add(db_changelog)
        # db.commit()
        # db.refresh(db_changelog)
        #
        # random_time = datetime.datetime.strptime(random_date("9/1/2022 1:30 PM", "9/18/2022 4:50 PM", random.random()),
        #                                          '%m/%d/%Y %I:%M %p')
        #
        # db_changelog = ChangeLog(
        #     created_at=random_time,
        #     location_id=return_obj.id,
        #     action_type=1,
        #     old_flags={"electricity": "Переривчаста", "fuelStation": "зачинено"},
        #     new_flags={"electricity": "Стабільна", "fuelStation": "відчинено"}
        # )
        # db.add(db_changelog)
        # db.commit()
        # db.refresh(db_changelog)
        #
        # random_time = datetime.datetime.strptime(random_date("9/1/2022 1:30 PM", "9/18/2022 4:50 PM", random.random()),
        #                                          '%m/%d/%Y %I:%M %p')
        #
        # db_changelog = ChangeLog(
        #     created_at=random_time,
        #     location_id=return_obj.id,
        #     action_type=2,
        #     media_url="http://static.prsa.pl/images/22f26b47-af71-4daa-a669-07f10bc23810.jpg"
        # )
        # db.add(db_changelog)
        # db.commit()
        # db.refresh(db_changelog)

        return db.query(Location).get(db_obj.id)

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
                Location.lng.between(lng["lo"], lng["hi"])).all()
                #Location.status === 3


def get_locations_awaiting_reports(db: Session, limit: int = 20, skip: int = 0) -> List[Location]:
    return db.query(Location).filter(Location.status == 1)\
        .order_by(desc(Location.created_at))\
        .limit(limit)\
        .offset(skip * limit)


def submit_location_reports(db: Session, *, obj_in: LocationReports) -> Any:

    location = db.query(Location).get(obj_in.location_id)

    if not location:
        return None

    reports = {
        "buildingCondition": obj_in.building_condition,
        "electricity": obj_in.electricity,
        "carEntrance": obj_in.car_entrance,
        "water": obj_in.water,
        "fuelStation": obj_in.fuel_station,
        "hospital": obj_in.hospital,
    }

    old_reports = location.reports
    new_reports = reports

    location.reports = reports

    # TODO confirmation for this?
    location.status = 3

    db.commit()
    db.refresh(location)

    changelog = create_changelog(db,
                                 location_id=location.id,
                                 old_object=old_reports,
                                 new_object=new_reports)

    # TODO rollback strategy if no changelog was created

    return location
