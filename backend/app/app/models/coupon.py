from email.policy import default
from typing import TYPE_CHECKING

from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401



# asset asociado a un cupon
class Asset(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    path = Column(String(128), nullable=True)  
    coupons = relationship("Coupon", back_populates="asset")
    #distance = Column(String, default="0")

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

# cupones de premios
class Coupon(Base):
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("asset.id"))
    asset = relationship("Asset", back_populates="coupons")

    name = Column(String)
    title = Column(String)
    description = Column(String)
    terms = Column(String)
    quantity = Column(Integer, default=0)
    expiration = Column(DateTime, nullable=False)
    
    # lng = Column(String, nullabled=True)
    # lat = Column(String, nullabled=True)
    time = Column(String, nullable=True, default=30)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    # coupon = relationship("CouponAssigned", back_populates="coupon")

# Cupon Asignado a un usuario
class CouponAssigned(Base):
    # id = Column(Integer, primary_key=True, index=True)
    coupon_id = Column(Integer, ForeignKey("coupon.id"), nullable=False, primary_key=True)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)
    # owner = relationship("User", back_populates="couponassigned")

    redeemed = Column(Boolean(), default=False)

    coupon = relationship("Coupon")
    owner = relationship('User')

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
