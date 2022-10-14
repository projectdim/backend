from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Organization(Base):

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=func.now())

    name = Column(String, nullable=False, unique=True)
    leader = Column(Integer, ForeignKey("user.id"))
    participants = relationship("User", back_populates="organization")
