from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Interval
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

import geopy.distance

from app.db.base_class import Base

status_list = {
    1: "Awaiting review",
    2: "Awaiting approval",
    3: "Approved"
}


class Location(Base):

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    report_expires = Column(DateTime)
    reported_by = Column(Integer, ForeignKey('user.id', ondelete="SET NULL"))
    status = Column(Integer, default=1)

    address = Column(String)
    street_number = Column(String)
    city = Column(String)
    country = Column(String)
    index = Column(Integer, nullable=False)
    lat = Column(Float)
    lng = Column(Float)
    reports = Column(JSONB) # Should we create a separate table for this??

    def calculate_distance(self, user_lat, user_lng):
        geolocation_coords = (user_lat, user_lng)
        location_coords = (self.lat, self.lng)

        return geopy.distance.geodesic(geolocation_coords, location_coords).km

    def to_json(self, user_lat=None, user_lng=None):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "address": self.address,
            "index": self.index,
            "city": self.city,
            "status": self.status,
            "country": self.country,
            "position": {
              "lat": self.lat, "lng": self.lng
            },
            "street_number": self.street_number,
            "distance": self.calculate_distance(user_lat, user_lng) if user_lat and user_lng else None,
            "reported_by": self.reported_by,
            "report_expires": self.report_expires,
            "reports": self.reports
        }


