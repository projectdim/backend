from typing import Optional, List
import datetime

from pydantic import BaseModel, EmailStr

from app.schemas import UserRepresentation


class OrganizationBase(BaseModel):
    name: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None


class OrganizationOut(OrganizationBase):
    id: int
    created_at: datetime.datetime
    # leader: Optional[UserRepresentation]
    participants: Optional[List[UserRepresentation]]

    class Config:
        orm_mode = True


class OrganizationUserInvite(BaseModel):
    emails: List[EmailStr]
