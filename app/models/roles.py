from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base_class import Base


class Role(Base):
    id = Column(Integer, primary_key=True, index=True)

    verbose_name = Column(String, nullable=False, unique=True)
    permissions = Column(JSONB, default=[])


# TODO class-based approach?
presets = {

    "aid_worker": [
        "users:me",
        "users:edit",
        "locations:view",
        "locations:edit"
    ],

    "platform_administrator": [
        "users:create",
        "users:delete",
        "users:me",
        "users:edit",
        "users:roles",
        "locations:view",
        "locations:edit",
        "locations:delete",
        "organizations:create",
        "organizations:view",
        "organizations:edit",
        "organizations:delete",
        "roles:read"
    ]
}
