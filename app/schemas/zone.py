

from pydantic import BaseModel


class ZoneBase(BaseModel):
    zone_type: int
    value: str
