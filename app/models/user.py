from app.db.base_class import Base
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import JSONB

role_permissions = {
    "aid_worker": ["locations:edit", "users:me", "users:edit"],
    "superadmin": ["locations:view", "locations:delete", "users:me", "users:edit"]
}


class User(Base):

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=datetime.now())

    username = Column(String, unique=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=False)

    email_confirmed = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)
    role = Column(String, nullable=False)

    permissions = Column(JSONB, default={})

