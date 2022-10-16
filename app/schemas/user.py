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
    organization: Optional[str]
    email_confirmed: bool
    role: str

    class Config:
        orm_mode = True


class UserRepresentation(UserBase):
    id: int
    organization: Optional[str]

    class Config:
        orm_mode = True
