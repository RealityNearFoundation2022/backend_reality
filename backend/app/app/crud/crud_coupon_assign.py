from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.coupon import CouponAssigned
from app.schemas.coupon import CouponAssignedCreate, CouponAssignedUpdate


class CRUDCouponAssigned(CRUDBase[CouponAssigned, CouponAssignedCreate, CouponAssignedUpdate]):
    def create_with_owner_and_coupon(
        self, db: Session, *, obj_in: CouponAssignedCreate, owner_id: int, coupon_id: int
    ) -> CouponAssigned:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id, coupon_id=coupon_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_owner_and_coupon(
        self, db: Session, *, owner_id: int, coupon_id: int
    ) -> List[CouponAssigned]:
        return (
            db.query(self.model)
            .filter(CouponAssigned.owner_id == owner_id, CouponAssigned.coupon_id == coupon_id)
            .first()
        )
    
    def get_by_owner_and_coupon_valid(
        self, db: Session, *, owner_id: int, coupon_id: int
    ) -> List[CouponAssigned]:
        return (
            db.query(self.model)
            .filter(CouponAssigned.owner_id == owner_id, CouponAssigned.coupon_id == coupon_id, CouponAssigned.redeemed == False)
            .first()
        )

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[CouponAssigned]:
        return (
            db.query(self.model)
            .filter(CouponAssigned.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_last_by_coupon(
        self, db: Session, *, coupon_id: int
    ) -> int:
        return (
            db.query(self.model)
            .filter(CouponAssigned.coupon_id == coupon_id)
            .order_by(CouponAssigned.created_at.desc())
            .first()
        )
    
    def count_by_coupon(
        self, db: Session, *, coupon_id: int
    ) -> int:
        return (
            db.query(self.model)
            .filter(CouponAssigned.coupon_id == coupon_id)
            .count()
        )

couponassigned = CRUDCouponAssigned(CouponAssigned)
