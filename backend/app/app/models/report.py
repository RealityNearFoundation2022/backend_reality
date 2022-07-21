from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Report(Base):
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    title = Column(String)
    description = Column(String)
    image = Column(String, default=0)
    status = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="reports")
