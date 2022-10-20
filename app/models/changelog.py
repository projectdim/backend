from app.db.base_class import Base

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB


class ChangeLog(Base):

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=func.now())
    location_id = Column(Integer, ForeignKey('location.id', ondelete="CASCADE"))
    action_type = Column(Integer, nullable=False)

    old_flags = Column(JSONB, nullable=True)
    new_flags = Column(JSONB, nullable=True)

