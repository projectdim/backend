from typing import Optional, Dict, Union
from typing_extensions import TypedDict
from datetime import datetime

from pydantic import BaseModel

from app.schemas import report

# TODO LocationOut class with typed dict position (check to_json location method)


class LocationBase(BaseModel):
    address: Optional[str] = None
    street_number: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    index: Optional[int] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class LocationCreate(LocationBase):
    # address: Optional[str] = None
    lat: float
    lng: float
    # index: Optional[int] = None
    # city: Optional[str] = None
    # country: Optional[str] = None


class LocationSearch(LocationBase):
    lat: Dict
    lng: Dict


class TestLocationSearch(BaseModel):
    lat: float
    lng: float
    zoom: Optional[int]


class LocationOut(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    address: Optional[str] = None
    street_number: Optional[str] = None
    index: Optional[str] = None
    city: Optional[str] = None
    status: int
    country: Optional[str] = None
    position: Dict
    reports: Optional[Dict] = None
    distance: Optional[int] = None

    class Config:
        orm_mode = True


class LocationAdmin(LocationOut):
    reported_by: int
    report_expires: datetime


# TODO convert to dataclasses with default vals
class LocationReports(BaseModel):
    location_id: int
    street_number: Optional[str] = None
    address: Optional[str] = None
    buildingCondition: report.BuildingReport
    electricity: report.ElectricityReport
    carEntrance: report.CarEntranceReport
    water: report.WaterReport
    fuelStation: report.FuelStationReport
    hospital: report.HospitalReport

