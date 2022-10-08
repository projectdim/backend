from app.db.base_class import Base

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB


class ChangeLog(Base):

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=datetime.now())
    location_id = Column(Integer, ForeignKey('location.id'))
    action_type = Column(Integer, nullable=False)

    old_flags = Column(JSONB, nullable=True)
    new_flags = Column(JSONB, nullable=True)
    media_url = Column(String, nullable=True)

