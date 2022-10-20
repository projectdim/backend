from typing import List, Any, Optional

from sqlalchemy.orm import Session

import pygeohash as pgh

from app.models import GeospatialIndex


def create_index(db: Session, location_id: int, lat: float, lng: float, status: int) -> GeospatialIndex:

    db_obj = GeospatialIndex(
        location_id=location_id,
        geohash=pgh.encode(lat, lng, 12),
        lat=lat,
        lng=lng,
        status=status
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return db_obj


def search_indexes_in_range(db: Session, lat: float, lng: float, zoom: int = 6) -> List[GeospatialIndex]:

    # Use zoom as precision points?
    # TODO check google api

    geohash = pgh.encode(lat, lng, 2)

    # print(f"Geohash : {geohash}")
    query = "{}%".format(geohash)
    # print(f"Query : {query}")

    return db.query(GeospatialIndex).filter(GeospatialIndex.geohash.like(query)).all()



