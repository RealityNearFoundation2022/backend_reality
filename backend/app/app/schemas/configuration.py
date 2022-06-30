from typing import Optional

from pydantic import BaseModel


# Shared properties
class ConfigurationBase(BaseModel):
    location_enabled: int


# Properties to receive on Configuration creation
class ConfigurationCreate(ConfigurationBase):
    owner_id: int


# Properties to receive on Configuration update
class ConfigurationUpdate(ConfigurationBase):
    pass


# Properties shared by models stored in DB
class ConfigurationInDBBase(ConfigurationBase):
    id: int
    location_enabled: int
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Configuration(ConfigurationInDBBase):
    pass


# Properties properties stored in DB
class ConfigurationInDB(ConfigurationInDBBase):
    pass
