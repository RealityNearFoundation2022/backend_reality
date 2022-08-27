from typing import Optional

from app.models.mongo import PyObjectId
from pydantic import BaseModel, Field
from bson import ObjectId


class EventModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Lutta livre expose"
            }
        }

class UpdateEventModel(BaseModel):
    name: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe"
            }
        }