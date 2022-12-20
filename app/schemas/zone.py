

from pydantic import BaseModel


class ZoneBase(BaseModel):
    zone_type: int
    value: str


class ZoneOut(ZoneBase):
    id: int
    bounding_box: str
    
