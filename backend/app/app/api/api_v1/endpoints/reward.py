from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse

from app import crud, models, schemas 
from app.api import deps
from datetime import datetime, timedelta

router = APIRouter()

#create
@router.post("/", response_model=schemas.RewardInDBBase)
def create_reward(
    *,
    db: Session = Depends(deps.get_db),
    reward_in: schemas.RewardCreate
) -> Any:
    """
    Create new reward.
    """
    reward = crud.reward.create_with_owner(db, obj_in=reward_in)
    return reward


# get rewards by user
@router.get("/user/{user_id}", response_model=List[schemas.RewardInDBBase])
def read_rewards_by_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 10
) -> Any:
    """
    Retrieve rewards by user.
    """
    rewards = crud.reward.get_rewards_history_by_user(db, owner_id=user_id, skip=skip, limit=limit)
    return rewards

# get total balance by user
@router.get("/user/{user_id}/balance", response_model=dict)
def read_total_balance_by_user(
    user_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve total balance by user.
    """
    total_balance = crud.reward.get_total_balance_by_user(db, owner_id=user_id)
    return {"total_balance": total_balance}