from typing import Optional, Dict, Union
from typing_extensions import TypedDict
from datetime import datetime

from pydantic import BaseModel

from app.schemas import report

# TODO LocationOut class with typed dict position (check to_json location method)


class LocationBase(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    index: Optional[int] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


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


class Lat(BaseModel):
    lat: str


class Lng(BaseModel):
    lng: str


class LocationOut(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    address: str
    index: str
    city: str
    status: int
    country: str
    position: Dict
    reports: Optional[Dict] = None

    class Config:
        orm_mode = True


class LocationAdmin(LocationOut):
    reported_by: int
    report_expires: datetime


# TODO convert to dataclasses with default vals
class LocationReports(BaseModel):
    location_id: int
    buildingCondition: report.BuildingReport
    electricity: report.ElectricityReport
    carEntrance: report.CarEntranceReport
    water: report.WaterReport
    fuelStation: report.FuelStationReport
    hospital: report.HospitalReport
