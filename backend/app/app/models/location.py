from typing import TYPE_CHECKING

from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Location(Base):
    id = Column(Integer, primary_key=True, index=True)
    lng = Column(Integer, default=0)
    lat = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="locations")

    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())