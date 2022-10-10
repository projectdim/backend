from typing import Optional, Dict
from typing_extensions import TypedDict
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class LocationBase(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    index: Optional[int] = None
    # coordinates: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    reports: Optional[Dict] = None


class LocationCreate(LocationBase):
    address: str
    # coordinates: str
    lat: float
    lng: float
    index: int
    city: str
    country: str


class LocationSearch(LocationBase):
    # coordinates: str
    lat: Dict
    lng: Dict


class LocationUpdate(LocationBase):
    address: Optional[str] = None
    # coordinates: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    reports: Optional[Dict] = None
    index: Optional[int] = None


class BuildingConditionEnum(str, Enum):
    intact = "Неушкоджена"
    damaged = "Пошкоджена"
    none = "Зруйнована"


class BuildingReport(TypedDict):
    flag: BuildingConditionEnum
    description: str


class ElectricityEnum(str, Enum):
    stable = "Стабільна"
    intermittent = "Переривчаста"
    no_data = "Відсутня"


class ElectricityReport(TypedDict):
    flag: ElectricityEnum
    description: str


class CarEntranceEnum(str, Enum):
    accessible = "Доступне"
    inaccessible = "Недоступне"
    no_data = "Інформація відсутня"


class CarEntranceReport(TypedDict):
    flag: CarEntranceEnum
    description: str


class WaterEnum(str, Enum):
    stable = "Стабільна"
    unstable = "Нестабільна"
    no_data = "Інформація відсутня"


class WaterReport(TypedDict):
    flag: WaterEnum
    description: str


class FuelStationEnum(str, Enum):
    open = "Відчинено"
    closed = "Зачинено"
    no_data = "Інформація відсутня"


class FuelStationReport(TypedDict, total=False):
    flag: FuelStationEnum
    description: str
    distance: Optional[float]


class HospitalEnum(str, Enum):
    open = "Відчинено"
    closed = "Зачинено"
    no_data = "Інформація відсутня"


class HospitalReport(TypedDict, total=False):
    flag: HospitalEnum
    description: str
    distance: Optional[float]


# TODO convert to dataclasses with default vals
class LocationReports(BaseModel):
    location_id: int

    building_condition: BuildingReport
    electricity: ElectricityReport
    car_entrance: CarEntranceReport
    water: WaterReport
    fuel_station: FuelStationReport
    hospital: HospitalReport
