from typing import TYPE_CHECKING

from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401
    from .contact import Contact  # noqa: F401
    from .location import Location  # noqa: F401
    from .configuration import Configuration  # noqa: F401
    from .notification import Notification  # noqa: F401
    from .report import Report  # noqa: F401
    from .coupon import CouponAssigned # noqa: F401


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    path = Column(String(), nullable=True, default="")
    avatar = Column(String(), nullable=True, default="")

    items = relationship("Item", back_populates="owner")
    contacts = relationship("Contact", back_populates="owner")
    locations = relationship("Location", back_populates="owner")
    configurations = relationship("Configuration", back_populates="owner")
    notifications = relationship("Notification", back_populates="owner")
    reports = relationship("Report", back_populates="owner")
    coupon_assigned = relationship("CouponAssigned", back_populates="owner")

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
