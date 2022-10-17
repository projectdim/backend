from typing import Optional, Dict
from datetime import datetime

from pydantic import BaseModel


class ChangelogOut(BaseModel):

    id: int
    created_at: datetime
    action_type: int

    old_flags: Dict
    new_flags: Dict

    class Config:
        orm_mode = True