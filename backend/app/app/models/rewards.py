from email.policy import default
from typing import TYPE_CHECKING

from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Reward(Base):
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    description = Column(String)
    # category_id = Column(Integer, ForeignKey("rewardcategory.id"), nullable=False)
    quantity = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

# class RewardCategory(Base):
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     active = Column(Boolean, default=True)
#     created_by = Column(Integer, ForeignKey("user.id"), nullable=False)
#     created_at = Column(DateTime, nullable=False, default=datetime.utcnow())    