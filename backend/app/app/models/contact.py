from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.declarative import declared_attr

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Contact(Base):
    id = Column(Integer, primary_key=True, index=True)
    pending = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("user.id"))
    contact_id = Column(Integer)
    owner = relationship("User", back_populates="contacts")
    locked = Column(Integer, default=0)
    __table_args__ = (UniqueConstraint('owner_id', 'contact_id', name='_owner_contact_uc'),)
