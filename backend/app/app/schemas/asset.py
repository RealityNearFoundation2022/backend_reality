from typing import Any, Optional, List
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class AssetBase(BaseModel):
    name: str
    locations: Optional[List] = None

# Properties to receive on Asset creation
class AssetCreate(AssetBase):
    pass


# Properties to receive on Asset update
class AssetUpdate(AssetBase):
    path_1: str
    path_2: str


# Properties shared by models stored in DB
class AssetInDBBase(AssetBase):
    id: int
    name: str
    path_1: Optional[str]
    path_2: Optional[str]

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Asset(AssetInDBBase):
    pass


# Properties properties stored in DB
class AssetInDB(AssetInDBBase):
    pass
