from typing import Optional, List
from pydantic import BaseModel

from app.schemas import UserRepresentation


class OrganizationBase(BaseModel):
    name: Optional[str] = None


class OrganizationOut(OrganizationBase):
    id: int
    leader: Optional[UserRepresentation]
    participants: Optional[List[UserRepresentation]]

    class Config:
        orm_mode = True
