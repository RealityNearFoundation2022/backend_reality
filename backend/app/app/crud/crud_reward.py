from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.rewards import Reward  
from app.schemas.reward import RewardCreate, RewardUpdate

class CRUDReward(CRUDBase[Reward,RewardCreate, RewardUpdate]):
    def create_with_owner(
            self, db: Session, *, obj_in: RewardCreate, owner_id: int
    )-> Reward:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_rewards_history_by_user(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ):
        return (
            db.query(self.model)
            .filter(Reward.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
    def get_total_balance_by_user(
        self, db: Session, *, owner_id: int
    ):
        return (
            db.query(self.model)
            .filter(Reward.owner_id == owner_id)
            .count()
        )
    
    
