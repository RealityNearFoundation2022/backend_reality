from typing import Optional
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class AssetBase(BaseModel):
    name: str
    path: str


# Properties to receive on Asset creation
class AssetCreate(AssetBase):
    pass


# Properties to receive on Asset update
class AssetUpdate(AssetBase):
    pass


# Properties shared by models stored in DB
class AssetInDBBase(AssetBase):
    id: int
    name: str
    path: str

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
