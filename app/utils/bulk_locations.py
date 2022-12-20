from typing import List, Dict, Generator

from openpyxl import load_workbook
from sqlalchemy.orm import Session

from app.utils.geocoding import geocode_address
from app.db.session import SessionLocal
from app.models.location import Location
from app.crud.crud_geospatial import create_index
from app.crud.crud_user import get_by_email


def serialize_spreadsheet(spreadsheet) -> List[Dict]:
    locations = []
    for row in spreadsheet.iter_rows(min_row=2, min_col=2):
        location = {
            "address": row[0].value,
            "city": row[1].value,
            "country": row[2].value,
            "index": row[3].value,
            "reports": {
                "buildingCondition": {
                    "flag": row[4].value,
                    "description": row[10].value
                },
                "electricity": {
                    "flag": row[5].value,
                    "description": ""
                },
                "car_entrance": {
                    "flag": row[6].value,
                    "description": ""
                },
                "water": {
                    "flag": row[7].value,
                    "description": ""
                },
                "fuel_station": {
                    "flag": row[8].value,
                    "description": ""
                },
                "hospital": {
                    "flag": row[9].value,
                    "description": ""
                }
            }
        }
        if location["address"] is None:
            continue
        locations.append(location)
    return locations


def geocode_locations(locations: List[Dict]):

    geocoded_locations = []
    for location in locations:
        coordinates = geocode_address(location["address"], location["city"])
        if not coordinates:
            continue
        location["lat"] = coordinates.latitude
        location["lng"] = coordinates.longitude
        geocoded_locations.append(location)

    return geocoded_locations


def add_to_db(location):
    db: Session = SessionLocal()

    try:
        db_obj = Location(
            address=location.get('address'),
            index=location.get('index'),
            lat=location.get('lat'),
            lng=location.get('lng'),
            country=location.get('country'),
            city=location.get('city'),
            status=3,
            reports=location.get('reports')
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        index = create_index(db, location_id=db_obj.id, lat=db_obj.lat, lng=db_obj.lng, status=db_obj.status)

    except Exception as e:
        print(e)
        return None


def main(spreadsheet_path: str):
    wb2 = load_workbook(spreadsheet_path)
    sheet = wb2.active
    locations = serialize_spreadsheet(sheet)
    print('Finished serializing, total locations {}'.format(len(locations)))
    updated_locations = geocode_locations(locations)
    print('Finished geocoding, total locations {}'.format(len(updated_locations)))
    unregistered_locations = []
    for location in updated_locations:
        if not location.get('lat') or not location.get('lng'):
            continue
        loc = add_to_db(location)
        if not loc:
            unregistered_locations.append(location)

    print('Could not register {} locations.'.format(len(unregistered_locations)))


main('locations_hostomel.xlsx')
