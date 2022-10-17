from typing import List, Any, Optional
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import desc

import pygeohash as pgh


from app.crud.crud_changelogs import create_changelog
from app.models.location import Location
from app.models.geospatial_index import GeospatialIndex
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
            status=3,
            reports=populate_reports()
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        for i in range(3):
            submit_location_reports(db, obj_in=LocationReports(location_id=db_obj.id, **populate_reports()), user_id=12)

        index = GeospatialIndex(
            location_id=db_obj.id,
            geohash=pgh.encode(db_obj.lat, db_obj.lng, 5),
            lat=db_obj.lat,
            lng=db_obj.lng
        )
        db.add(index)
        db.commit()

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
    hash = pgh.encode(lat["lo"], lng["lo"], 5)
    # return db.query(Location)\
    #     .filter(Location.lat.between(lat["lo"], lat["hi"]),
    #             Location.lng.between(lng["lo"], lng["hi"])).all()
                #Location.status === 3
    return db.query(GeospatialIndex).filter(GeospatialIndex.geohash.like(hash)).all()


def get_locations_awaiting_reports_count(db: Session) -> int:
    return db.query(Location).filter(Location.status == 1, Location.reported_by == None).count()


def get_locations_awaiting_reports(db: Session, limit: int = 20, skip: int = 0) -> List[Location]:
    return db.query(Location).filter(Location.status == 1, Location.reported_by == None)\
        .order_by(desc(Location.created_at))\
        .limit(limit)\
        .offset(skip * limit).all()


def assign_report(db: Session, user_id: int, location_id: int) -> Optional[Location]:
    location = db.query(Location).get(location_id)

    if location.reported_by:
        return None

    location.reported_by = user_id
    location.report_expires = datetime.now() + timedelta(days=1)

    db.commit()
    db.refresh(location)
    return location


def remove_assignment(db: Session, location_id: int, user_id: int) -> Optional[Location]:
    location = db.query(Location).get(location_id)

    if location.reported_by != user_id or not location.reported_by:
        return None

    location.reported_by = None
    location.report_expires = None

    db.commit()
    db.refresh(location)
    return location


def get_user_assigned_locations(db: Session, user_id: int) -> List[Location]:
    return db.query(Location).filter(Location.reported_by == user_id, Location.status == 1).all()


def submit_location_reports(db: Session, *, obj_in: LocationReports, user_id: int) -> Any:

    location = db.query(Location).get(obj_in.location_id)

    if not location:
        return None

    reports = {
        "buildingCondition": obj_in.buildingCondition,
        "electricity": obj_in.electricity,
        "carEntrance": obj_in.carEntrance,
        "water": obj_in.water,
        "fuelStation": obj_in.fuelStation,
        "hospital": obj_in.hospital,
    }

    old_reports = location.reports
    new_reports = reports

    location.reports = reports

    # TODO confirmation for this?
    location.status = 3
    location.report_expires = None
    location.reported_by = user_id

    db.commit()
    db.refresh(location)

    changelog = create_changelog(db,
                                 location_id=location.id,
                                 old_object=old_reports,
                                 new_object=new_reports)

    # TODO rollback strategy if no changelog was created

    return location
