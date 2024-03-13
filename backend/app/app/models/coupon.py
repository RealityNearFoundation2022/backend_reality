from email.policy import default
from typing import TYPE_CHECKING

from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401



class AssetLocation(Base):
    id = Column(Integer, primary_key=True, index=True)
    lat = Column(String(128), nullable=True)
    lng = Column(String(128), nullable=True)
    rule = Column(String(128), nullable=True, default="")
    asset_id = Column(Integer, ForeignKey("asset.id"))
    asset = relationship("Asset", back_populates="locations")

# asset asociado a un cupon
class Asset(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    default = Column(Boolean, default=False)
    path = Column(String(128), nullable=True)
    path_2 = Column(String(128), nullable=True)
    # coupons = relationship("Coupon", back_populates="asset")
    coupon_id = Column(Integer, ForeignKey("coupon.id"), nullable=True, primary_key=True)
    locations = relationship("AssetLocation", back_populates="asset")
    #distance = Column(String, default="0")

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())



# cupones de app
class Coupon(Base):
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("couponcategory.id"), nullable=True)
    img = Column(String, nullable=True)
    name = Column(String)
    title = Column(String)
    description = Column(String)
    terms = Column(String)
    quantity = Column(Integer, default=0)
    expiration_date = Column(DateTime, nullable=False)
    start_date = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

class CouponCategory(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    img = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_by = Column(Integer, ForeignKey("user.id"), nullable=False)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())    
    


# Cupon Asignado a un usuario
class CouponAssigned(Base):
    id = Column(Integer, primary_key=True, index=True)
    coupon_id = Column(Integer, ForeignKey("coupon.id"), nullable=False, primary_key=True)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)
    coupon = relationship("Coupon")
    owner = relationship('User')
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

class CouponReedeemed(Base):
    id = Column(Integer, primary_key=True, index=True)
    coupon_id = Column(Integer, ForeignKey("coupon.id"), nullable=False, primary_key=True)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)
    admin_id = Column(Integer, nullable=False)
    coupon = relationship("Coupon")
    owner = relationship('User')
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

