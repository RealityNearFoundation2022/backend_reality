from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.coupon import Asset
from app.schemas.asset import AssetCreate, AssetUpdate


class CRUDAsset(CRUDBase[Asset, AssetCreate, AssetUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: AssetCreate, owner_id: int
    ) -> Asset:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Asset]:
        return (
            db.query(self.model)
            .filter(Asset.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


asset = CRUDAsset(Asset)
