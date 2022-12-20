from pydantic import BaseModel


class LocationRequestOtp(BaseModel):
    phone_number: str
    otp: str
    lat: float
    lng: float
