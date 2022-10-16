from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base_class import Base

role_permissions = {
    "aid_worker": ["locations:view", "locations:edit", "users:me", "users:edit"],
    "superadmin": ["locations:view", "locations:delete", "users:me", "users:edit"]
}


class User(Base):

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=func.now())

    username = Column(String)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    organization = Column(Integer, ForeignKey("organization.id", ondelete="SET NULL"))

    hashed_password = Column(String)

    email_confirmed = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)

    permissions = Column(JSONB, default={})
    role = Column(String, nullable=False)

    registration_token = Column(String)
    registration_token_expires = Column(DateTime)

    password_renewal_token = Column(String)
    password_renewal_token_expires = Column(DateTime)

    assigned_locations = relationship("Location")

