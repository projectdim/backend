from typing import Optional, Dict
from typing_extensions import TypedDict
from datetime import datetime

from pydantic import BaseModel

from app.schemas import report

# TODO LocationOut class with typed dict position (check to_json location method)


class LocationBase(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    index: Optional[int] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    reports: Optional[Dict] = None


class LocationCreate(LocationBase):
    address: str
    lat: float
    lng: float
    index: int
    city: str
    country: str


class LocationSearch(LocationBase):
    lat: Dict
    lng: Dict


class LocationUpdate(LocationBase):
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    reports: Optional[Dict] = None
    index: Optional[int] = None


# TODO convert to dataclasses with default vals
class LocationReports(BaseModel):
    location_id: int
    building_condition: report.BuildingReport
    electricity: report.ElectricityReport
    car_entrance: report.CarEntranceReport
    water: report.WaterReport
    fuel_station: report.FuelStationReport
    hospital: report.HospitalReport
