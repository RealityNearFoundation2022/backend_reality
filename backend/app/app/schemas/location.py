from typing import Optional

from pydantic import BaseModel


# Shared properties
class LocationBase(BaseModel):
    location_enabled: int


# Properties to receive on Location creation
class LocationCreate(LocationBase):
    owner_id: int


# Properties to receive on Location update
class LocationUpdate(LocationBase):
    pass


# Properties shared by models stored in DB
class LocationInDBBase(LocationBase):
    id: int
    location_enabled: int
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Location(LocationInDBBase):
    pass


# Properties properties stored in DB
class LocationInDB(LocationInDBBase):
    pass
