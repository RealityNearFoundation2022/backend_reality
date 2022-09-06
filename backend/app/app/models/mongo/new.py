from typing import List, Optional

from app.models.mongo import PyObjectId
from pydantic import BaseModel, Field
from bson import ObjectId


class ArticlesModel(BaseModel):
    data: str = Field(...)
    image: str = Field(...)


class NewModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    image: str = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    planners: str = Field(...)
    date: str = Field(...)
    url: Optional[str] = None
    # articles: Optional[List[ArticlesModel]] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Lutta livre expose",
                "image": "",
                "title": "",
                "description": "",
                "planners": "",
                "date": "",
                "url": ""
                # "articles": [
                #     {
                #         "data": ""
                #     },
                #     {
                #         "data": ""
                #     }
                # ]
            }
        }


class CreateNewModel(NewModel):
    articles: Optional[List[ArticlesModel]] = None


class ListNewModel(NewModel):
    articles: Optional[List[ArticlesModel]] = None


class UpdateNewModel(BaseModel):
    image: str = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    planners: str = Field(...)
    date: str = Field(...)
    url: Optional[str] = None
    # articles: List[ArticlesModel] = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Lutta livre expose",
                "image": "",
                "title": "",
                "description": "",
                "planners": "",
                "date": "",
                "url": "",
                # "articles": [
                #     {
                #         "data": "",
                #         "image": ""
                #     },
                #     {
                #         "data": "",
                #         "image": ""
                #     }
                # ]
            }
        }
