from app.db.base_class import Base
from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.config import settings


class SessionHistory(Base):

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, default=func.now() + timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    # Is this always unique??
    access_token = Column(String, nullable=False, unique=True)

    user_agent = Column(String)
    user_ip = Column(String)

    is_active = Column(Boolean(), default=True)
