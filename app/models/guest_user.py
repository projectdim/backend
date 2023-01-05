from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GuestUser(Base):

    id = Column(Integer, primary_key=True, index=True)

    phone_number = Column(String, nullable=False, unique=True)

    last_request = Column(DateTime, nullable=True)
    total_otp_requests = Column(Integer, default=0)

    location_requests = relationship("Location")
