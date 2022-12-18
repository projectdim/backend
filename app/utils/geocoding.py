from typing import Any

from geopy.geocoders import GoogleV3, Nominatim
import osmnx as ox
from shapely.geometry import Point


geocoder = Nominatim(user_agent="GetLoc")


def geocode_address(address: str, city: str) -> Any:

    try:
        coordinates = geocoder.geocode('{}, {}'.format(address, city), country_codes='ua')
        print(coordinates)
        return coordinates

    except Exception as e:
        print(e)
        return None


def reverse(lat: float, lng: float) -> Any:

    try:
        address = geocoder.reverse('{}, {}'.format(lat, lng))
        # print(address)
        print(address.raw)
        return address.raw["address"]

    except Exception as e:
        print(e)
        return None


def get_bounding_box_by_region_name(region_name: str):

    try:
        gdf = ox.geocode_to_gdf(region_name)
        geom = gdf.loc[0, 'geometry']
        return geom

    except ValueError:
        return None


def check_intersection(geom, coords):
    return geom.intersects(Point(coords))

