from typing import Any, Optional
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class AssetLocationBase(BaseModel):
    lng: str
    lat: str
    rule: Optional[str]


# Properties to receive on AssetLocation creation
class AssetLocationCreate(AssetLocationBase):
    pass


# Properties to receive on AssetLocation update
class AssetLocationUpdate(AssetLocationBase):
    pass


# Properties shared by models stored in DB
class AssetLocationInDBBase(AssetLocationBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class AssetLocation(AssetLocationInDBBase):
    pass


# Properties properties stored in DB
class AssetLocationInDB(AssetLocationInDBBase):
    pass
