from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.coupon import Coupon
from app.schemas.coupon import CouponCreate, CouponUpdate


class CRUDCoupon(CRUDBase[Coupon, CouponCreate, CouponUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: CouponCreate, owner_id: int
    ) -> Coupon:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_with_asset(
        self, db: Session, *, obj_in: CouponCreate, asset_id: int
    ) -> Coupon:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, asset_id=asset_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Coupon]:
        return (
            db.query(self.model)
            .filter(Coupon.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


coupon = CRUDCoupon(Coupon)
