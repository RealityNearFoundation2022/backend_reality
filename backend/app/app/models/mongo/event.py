from datetime import datetime
from typing import Optional, List

from app.models.mongo import PyObjectId
from pydantic import BaseModel, Field
from bson import ObjectId


class LocationModel(BaseModel):
    lat: Optional[str] = None
    lng: Optional[str] = None
    address: Optional[str] = None

class MediaModel(BaseModel):
    guid: str = Field(...)
    type: str = Field(...)
    path: str = Field(...)

class EventModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    description: str = Field(...)
    planners: str = Field(...)
    date: str = Field(...)
    long_description: str = Field(...)
    # media: List[Optional[MediaModel]] = Field(...)
    url: str = Field(...)
    location: Optional[LocationModel] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Lutta livre expose",
                "description": "",
                "planners": "",
                "date": "",
                "long_description": "",
                "url": "nuruk"
            }
        }

class EventModelCreate(EventModel):
    media: List[MediaModel] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Lutta livre expose",
                "description": "",
                "planners": "",
                "date": "",
                "long_description": "",
                "media": [{
                    "guid": "guid",
                    "type": "image",
                    "path": ""
                },
                {
                    "guid": "guid",
                    "type": "video",
                    "path": ""
                }],
                "url": "nuruk",
                "location": {
                    "lng": "111111111",
                    "lat": "333333333",
                    "address": "calle 5 la plata - buenos aires - argentina"
                }
            }
        }


class ListEventModel(EventModel):
    media: Optional[List[MediaModel]] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Lutta livre expose",
                "description": "",
                "planners": "",
                "date": "",
                "long_description": "",
                "media": [{
                    "guid": "guid",
                    "type": "image",
                    "path": ""
                },
                {
                    "guid": "guid",
                    "type": "video",
                    "path": ""
                }],
                "url": "nuruk",
                "location": {
                    "lng": "111111111",
                    "lat": "333333333",
                    "address": "calle 5 la plata - buenos aires - argentina"
                }
            }
        }

class UpdateEventModel(BaseModel):
    title: Optional[str] = Field(...)
    description: Optional[str] = Field(...)
    planners: Optional[str] = Field(...)
    date: Optional[str] = Field(...)
    long_description: Optional[str] = Field(...)
    # media: Optional[List[MediaModel]] = Field(...)
    url: Optional[str] = Field(...)
    location: Optional[LocationModel] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Lutta livre expose",
                "description": "",
                "planners": "",
                "date": "",
                "long_description": "",
                "url": "nuruk",
                "location": {
                    "lng": "111111111",
                    "lat": "333333333",
                    "address": "calle 5 la plata - buenos aires - argentina"
                }
            }
        }