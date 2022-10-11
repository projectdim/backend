from typing_extensions import TypedDict
from typing import Optional

from app.schemas import enums


class BuildingReport(TypedDict):
    flag: enums.BuildingConditionEnum
    description: str


class ElectricityReport(TypedDict):
    flag: enums.ElectricityEnum
    description: str


class CarEntranceReport(TypedDict):
    flag: enums.CarEntranceEnum
    description: str


class WaterReport(TypedDict):
    flag: enums.WaterEnum
    description: str


class FuelStationReport(TypedDict, total=False):
    flag: enums.FuelStationEnum
    description: str
    distance: Optional[float]


class HospitalReport(TypedDict, total=False):
    flag: enums.HospitalEnum
    description: str
    distance: Optional[float]
