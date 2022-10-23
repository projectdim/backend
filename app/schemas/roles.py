from typing import List, Optional

from pydantic import BaseModel


class UserRole(BaseModel):

    verbose_name: str
    permissions: List[str]
