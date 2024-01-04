from typing import List

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.coupon import Coupon, CouponCategory, CouponReedeemed
from app.schemas.coupon import CuponCreate, CuponUpdate, CuponCategoryCreate, CuponCategoryUpdate, CouponReedeemedCreate
from datetime import datetime


class CRUDCoupon(CRUDBase[Coupon, CuponCreate, CuponUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: CuponCreate, owner_id: int
    ) -> Coupon:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    #update coupon
    def update_with_owner(
        self, db: Session, *, db_obj: Coupon, obj_in: CuponUpdate
    ) -> Coupon:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
            

    def get_all_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Coupon]:
        return (
            db.query(self.model)
            .filter(Coupon.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    

    #get all coupons to user if is active and date is valid between start and expiration
    def get_all_to_user(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Coupon]:
        return (
            db.query(self.model)
            .filter(Coupon.active == True)
            .filter(Coupon.start_date <= datetime.utcnow())
            .filter(Coupon.expiration_date >= datetime.utcnow())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    #get all coupons to user if is active and date is valid between start and expiration and category
    def get_all_to_user_by_category(
        self, db: Session, *, category_id: int, skip: int = 0, limit: int = 100
    ) -> List[Coupon]:
        return (
            db.query(self.model)
            .filter(Coupon.active == True)
            .filter(Coupon.start_date <= datetime.utcnow())
            .filter(Coupon.expiration_date >= datetime.utcnow())
            .filter(Coupon.category_id == category_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    #get all categories if is active
    def get_all_categories(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[CouponCategory]:
        return (
            db.query(CouponCategory)
            .filter(CouponCategory.active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    #redeem coupon with validations
    #user redeem coupon if is active and date is valid between start and expiration
    #user redeem coupon if quantity is greater than 0 (quantity calculated with couponredeemed table and compare with quantity in coupon table)
    #user redeem coupon if user has not redeemed the coupon
    #Devuelve un string con el resultado de la operacion
    def redeem_coupon(
        self, db: Session, *, obj_in: CouponReedeemedCreate
    ) -> dict:
        coupon = db.query(Coupon).filter(Coupon.id == obj_in.coupon_id).first()
        quantity_redeemed = db.query(CouponReedeemed).filter(CouponReedeemed.coupon_id == obj_in.coupon_id).count()
        if coupon is None:
            raise HTTPException(status_code=404, detail="Cupon no encontrado")
        if coupon.active == False:
            raise HTTPException(status_code=404, detail="Cupon no activo")
        if coupon.start_date > datetime.utcnow() or coupon.expiration_date < datetime.utcnow():
            raise HTTPException(status_code=404, detail="Cupon fuera de fecha")
        if quantity_redeemed >= coupon.quantity:
            raise HTTPException(status_code=404, detail="Cupon agotado")
        coupon_redeemed = db.query(CouponReedeemed).filter(CouponReedeemed.coupon_id == obj_in.coupon_id).filter(CouponReedeemed.owner_id == obj_in.owner_id).first()
        if coupon_redeemed is not None:
            raise HTTPException(status_code=404, detail="Cupon ya reclamado")
        coupon_redeemed = CouponReedeemed(coupon_id=obj_in.coupon_id, owner_id=obj_in.owner_id, admin_id=obj_in.admin_id)
        db.add(coupon_redeemed)
        db.commit()
        return {"message": "Cupon reclamado exitosamente"}
    
    
    
    

coupon = CRUDCoupon(Coupon)
category = CRUDCoupon(CouponCategory)
redeemed = CRUDCoupon(CouponReedeemed)
