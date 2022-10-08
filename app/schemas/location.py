from typing import Optional, Dict
from datetime import datetime

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
