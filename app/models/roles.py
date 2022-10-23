from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base_class import Base


class Role(Base):
    id = Column(Integer, primary_key=True, index=True)

    verbose_name = Column(String, nullable=False, unique=True)
    permissions = Column(JSONB, default=[])
