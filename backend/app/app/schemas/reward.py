from typing import Optional, Any
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class RewardBase(BaseModel):
    owner_id: Optional[int] = None
    description: str
    quantity: int

class RewardInDBBase(RewardBase):
    id: int
    owner_id: int
    description: str
    quantity: int
    class Config:
        orm_mode = True


class RewardCreate(RewardBase):
    pass

class RewardUpdate(RewardBase):
    pass

