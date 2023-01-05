from typing import List, Any, Optional
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.crud.crud_changelogs import create_changelog
from app.crud.crud_geospatial import create_index
from app.models.location import Location
from app.models.user import User
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

        index = create_index(db, location_id=db_obj.id, lat=obj_in.lat, lng=obj_in.lng, status=db_obj.status)

        return db.query(Location).get(db_obj.id)

    except Exception as e:
        print(e)
        return None


def create_location_review_request(
        db: Session,
        *,
        address: dict,
        lat: float,
        lng: float,
        requested_by: int = None
) -> Optional[Location]:

    try:
        db_obj = Location(
            address=address.get('road', None),
            street_number=address.get('house_number', None),
            city=address.get('city', address.get('town', address.get('village', None))),
            country=address.get('country', None),
            index=address.get('postcode', None),
            lat=lat,
            lng=lng,
            status=1,
            requested_by=requested_by
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        index = create_index(db, location_id=db_obj.id, lat=lat, lng=lng, status=db_obj.status)

        return db_obj

    except Exception as e:
        print(e)
        return None


# def create_location_review_request(db: Session, *, obj_in: LocationCreate) -> Optional[Location]:
#
#     try:
#         db_obj = Location(
#             address=obj_in.address,
#             index=obj_in.index,
#             lat=obj_in.lat,
#             lng=obj_in.lng,
#             status=1,
#             country=obj_in.country,
#             city=obj_in.city,
#         )
#
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#
#         index = create_index(db, location_id=db_obj.id, lat=obj_in.lat, lng=obj_in.lng, status=db_obj.status)
#
#         return db_obj
#
#     except Exception as e:
#         print(e)
#         return None


def get_location_by_id(db: Session, location_id: int) -> Location:
    return db.query(Location).get(location_id)


def get_location_by_coordinates(db: Session, lat: float, lng: float) -> Location:
    return db.query(Location).filter(Location.lat == lat, Location.lng == lng).first()


def get_locations_awaiting_reports_count(db: Session) -> int:
    return db.query(Location).filter(Location.status == 1, Location.reported_by == None).count()


def get_locations_awaiting_reports(db: Session, limit: int = 20, skip: int = 0) -> List[Location]:
    return db.query(Location).filter(Location.status == 1, Location.reported_by == None)\
        .order_by(desc(Location.created_at))\
        .limit(limit)\
        .offset(skip * limit).all()


def get_all_locations(db: Session) -> List[Location]:
    return db.query(Location).all()


def assign_report(db: Session, user_id: int, location_id: int) -> Optional[Location]:
    location = db.query(Location).get(location_id)

    if location.reported_by:
        return None

    location.reported_by = user_id
    location.report_expires = datetime.now() + timedelta(days=1)

    user = db.query(User).get(user_id)
    user.last_activity = datetime.now()

    db.commit()
    db.refresh(location)
    return location


def remove_assignment(db: Session, location_id: int, user_id: int) -> Optional[Location]:
    location = db.query(Location).get(location_id)

    if location.reported_by != user_id or not location.reported_by:
        return None

    location.reported_by = None
    location.report_expires = None

    user = db.query(User).get(user_id)
    user.last_activity = datetime.now()

    db.commit()
    db.refresh(location)
    return location


def get_user_assigned_locations(db: Session, user_id: int) -> List[Location]:
    return db.query(Location).filter(Location.reported_by == user_id, Location.status == 1).all()


def submit_location_reports(db: Session, *, obj_in: LocationReports, user_id: int) -> Any:

    location = db.query(Location).get(obj_in.location_id)

    if not location:
        return None

    # if not location.address:
    if obj_in.address:
        location.address = obj_in.address

    # if not location.street_number:
    if obj_in.street_number:
        location.street_number = obj_in.street_number

    if obj_in.city:
        location.city = obj_in.city

    if obj_in.index:
        location.index = obj_in.index

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

    # update location record
    location.status = 3
    location.report_expires = None
    location.reported_by = user_id

    # update
    index_record = db.query(GeospatialIndex).filter(GeospatialIndex.location_id == obj_in.location_id).first()
    index_record.status = 3

    user = db.query(User).get(user_id)
    user.last_activity = datetime.now()

    db.commit()
    db.refresh(location)

    changelog = create_changelog(db,
                                 location_id=location.id,
                                 old_object=old_reports,
                                 new_object=new_reports)


    # TODO rollback strategy if no changelog was created

    return location


def get_activity_feed(db: Session, records: int = 10) -> List[Location]:
    return db.query(Location).filter(Location.status == 3).order_by(desc(Location.created_at)).limit(records)


def delete_location(db: Session, location_id: int) -> Optional[Location]:

    location = get_location_by_id(db, location_id=location_id)

    db.delete(location)
    db.commit()
    return get_location_by_id(db, location_id=location_id)


def drop_locations(db: Session):
    try:
        db.query(Location).delete()
        db.commit()
        return None

    except Exception as e:
        print(e)
        return
