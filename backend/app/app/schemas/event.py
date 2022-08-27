from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


# Shared properties
class EventsBase(BaseModel):
    id: int = Field(..., alias='_id')
    #image: str
    #title: str
    #description: str
    #organizers: str
    #lng: str
    #lat: str
    #date: str
    #description_long: str
    #media: str
    #url: str


# Properties to receive on Events creation
class EventsCreate(EventsBase):
    pass


# Properties to receive on Events update
class EventsUpdate(EventsBase):
    pass


# Properties shared by models stored in DB
class EventsInDBBase(EventsBase):
    # id: int
    image: str
    title: str
    description: str
    organizers: str
    lng: str
    lat: str
    date: str
    description_long: str
    media: str
    url: str

    # created_at: datetime
    # updated_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Events(EventsInDBBase):
    pass


# Properties properties stored in DB
class EventsInDB(EventsInDBBase):
    pass
