from typing import Optional, Any
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class CuponBase(BaseModel):
    owner_id: Optional[int] = None
    img: str
    name: str
    title: str
    description: str
    terms: str
    quantity: int
    expiration_date: str
    start_date: str
    active: bool

class CuponInDBBase(CuponBase):
    id: int
    owner_id: int
    img: str
    name: str
    title: str
    description: str
    terms: str
    quantity: int
    expiration_date: datetime
    start_date: datetime
    active: bool
    class Config:
        orm_mode = True


class CuponCreate(CuponBase):
    pass

class CuponUpdate(CuponBase):
    pass

class CuponCategoryBase(BaseModel):
    name: str
    img: str
    active: bool
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class CuponCategoryInDBBase(CuponCategoryBase):
    id: int
    name: str
    img: str
    active: bool
    class Config:
        orm_mode = True

class CuponCategoryCreate(CuponCategoryBase):
    pass

class CuponCategoryUpdate(CuponCategoryBase):
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


#
class CouponAssigned(CouponAssignedInDBBase):
    pass


class CouponReedeemedBase(BaseModel):
    coupon_id: int
    owner_id: int
    admin_id: int

class CouponReedeemedCreate(CouponReedeemedBase):
    pass

class CouponReedeemedUpdate(CouponReedeemedBase):
    pass

class CouponReedeemedInDBBase(BaseModel):
    coupon_id: int
    owner_id: int
    admin_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
