from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Notification(Base):
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Integer, default=0)
    read = Column(Integer, default=0)
    data = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="notifications")


