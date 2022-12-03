from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.coupon import AssetLocation
from app.schemas.assetlocation import AssetLocationCreate, AssetLocationUpdate


class CRUDAssetLocation(CRUDBase[AssetLocation, AssetLocationCreate, AssetLocationUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: AssetLocationCreate, owner_id: int
    ) -> AssetLocation:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[AssetLocation]:
        return (
            db.query(self.model)
            .filter(AssetLocation.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_asset(
        self, db: Session, *, obj_in: AssetLocationCreate, asset_id: int 
    ) -> int:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, asset_id=asset_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return asset_id

asset_location = CRUDAssetLocation(AssetLocation)
