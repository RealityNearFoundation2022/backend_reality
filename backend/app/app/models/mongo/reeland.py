from typing import List, Optional

from app.models.mongo import PyObjectId
from pydantic import BaseModel, Field
from bson import ObjectId



class ReelandModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    x: str = Field(...)
    y: str = Field(...)
    price: str = Field(...)
    disabled: Optional[bool] = False
    description: str = Field(...)
    color: Optional[str] = "#green"
    owner: Optional[str] = None
    link: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "x": "1",
                "y": "2",
                "price": "1000",
                "disabled": "false",
                "description": "plaza central",
                "color": "#green",
                "owner": "reality.near",
                "link": "/1.1.1.1/4.4.4.4"
            }
        }


class CreateReelandModel(ReelandModel):
    pass


class ListReelandModel(ReelandModel):
    pass


class UpdateReelandModel(BaseModel):
    x: str = Field(...)
    y: str = Field(...)
    price: str = Field(...)
    disabled: Optional[bool] = False
    description: str = Field(...)
    color: Optional[str] = "#green"
    owner: Optional[str] = None
    link: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "x": "1",
                "y": "2",
                "price": "1000",
                "disabled": "false",
                "description": "plaza central",
                "color": "#green",
                "owner": "reality.near",
                "link": "/1.1.1.1/4.4.4.4"
            }
        }
