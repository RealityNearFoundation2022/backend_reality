from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List

from app.crud.base import CRUDBase
from app.models.rewards import Reward  
from app.schemas.reward import RewardCreate, RewardUpdate

class CRUDReward(CRUDBase[Reward,RewardCreate, RewardUpdate]):
    def create_with_owner(
            self, db: Session, *, obj_in: RewardCreate
    )-> Reward:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_rewards_history_by_user(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    )-> List[Reward]:
        return (
            db.query(self.model)
            .filter(Reward.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
    def get_total_balance_by_user(
        self, db: Session, *, owner_id: int
    )-> dict:
        #get rewards from user and return the sum of all rewards
        rewards = db.query(self.model).filter(Reward.owner_id == owner_id).all()
        balance = 0
        for reward in rewards:
            balance += reward.quantity
        return balance
    
reward = CRUDReward(Reward)