from typing import Optional, List

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenBase(BaseModel):
    sub: Optional[str] = None
    scopes: List[str] = []
