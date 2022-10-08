from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class UserSession(BaseModel):
    id: int
    created_at: datetime
    expires_at: datetime
    user_agent: Optional[str]
    user_ip: Optional[str]

    class Config:
        orm_mode = True
