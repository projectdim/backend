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


class UserPasswordUpdate(BaseModel):
    old_password: str
    new_password: str


class UserOut(UserBase):
    id: int
    last_activity: Optional[datetime.datetime] = None
    organization: Optional[int]
    email_confirmed: bool
    is_active: bool
    role: str
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

    class Config:
        orm_mode = True
