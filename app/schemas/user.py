import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    organization: Optional[int]
    password: str


class UserInvite(BaseModel):
    email: EmailStr
    organization: int


class UserPasswordRenewal(BaseModel):
    access_token: str
    new_password: str


class UserPasswordUpdate(BaseModel):
    old_password: str
    new_password: str


class UserOrganizationDetails(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserOut(UserBase):
    id: int
    last_activity: Optional[datetime.datetime] = None
    organization: Optional[int]
    email_confirmed: bool
    is_active: bool
    role: str
    organization_model: Optional[UserOrganizationDetails] = None
    # TODO REMOVE
    registration_token: Optional[str] = None

    class Config:
        orm_mode = True


class UserRepresentation(UserBase):
    id: int
    last_activity: Optional[datetime.datetime] = None
    email_confirmed: bool
    is_active: bool
    organization: Optional[int]
    organization_model: Optional[UserOrganizationDetails] = None

    class Config:
        orm_mode = True
