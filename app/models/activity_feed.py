from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base_class import Base


# Do we even need such model?
class ActivityFeed(Base):
    id = Column(Integer, primary_key=True, index=True)

    location_id = Column(Integer, ForeignKey('location.id', ondelete="CASCADE"), nullable=False)
    full_address = Column(String, nullable=False)
    reports = Column(JSONB)
