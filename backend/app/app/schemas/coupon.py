from typing import Optional, Any
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class CouponBase(BaseModel):
    asset_id: int
    name: str
    title: str
    description: str
    terms: str
    quantity: int
    expiration: str
    time: str

# Properties to receive on Coupon creation
class CouponCreate(CouponBase):
    pass


# Properties to receive on Coupon update
class CouponUpdate(CouponBase):
    pass

# Shared properties
class CouponAssignedBase(BaseModel):
    coupon_id: int
    owner_id: int
    redeemed: bool = False

# Properties to receive on CouponAssigned creation
class CouponAssignedCreate(CouponAssignedBase):
    pass


# Properties to receive on CouponAssigned update
class CouponAssignedUpdate(CouponAssignedBase):
    pass



# Cupon Asignado a un usuario
class CouponAssignedInDBBase(BaseModel):
    coupon_id: int
    owner_id: int

    redeemed: bool = False

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Properties shared by models stored in DB
class CouponInDBBase(CouponBase):
    id: int
    asset_id: int
    name: str
    title: str
    description: str
    terms: str
    quantity: int
    expiration: datetime
    time: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Coupon(CouponInDBBase):
    asset: Any

#
class CouponAssigned(CouponAssignedInDBBase):
    pass

# Properties properties stored in DB
class CouponInDB(CouponInDBBase):
    pass


