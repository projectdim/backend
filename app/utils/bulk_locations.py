from typing import Optional, List, Dict

import requests

from openpyxl import load_workbook

from app.utils.geocoding import geocode_address


def custom_visicom_geocoder(address: str, city: str):
    r = requests.get(
        f'https://api.visicom.ua/data-api/5.0/uk/geocode.json?text={address}&country=ua'
    )
    print(r.status_code)
    print(r.json())


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
        locations.append(location)

    print(locations[0])
    return locations


def geocode_locations(locations: List[Dict]):

    for location in locations:
        coordinates = geocode_address(location["address"], location["city"])
        # custom_visicom_geocoder(location["address"], location["city"])


def main(spreadsheet_path: str):
    wb2 = load_workbook(spreadsheet_path)
    sheet = wb2.active
    locations = serialize_spreadsheet(sheet)
    geocode_locations(locations)


main('locations_hostomel.xlsx')
