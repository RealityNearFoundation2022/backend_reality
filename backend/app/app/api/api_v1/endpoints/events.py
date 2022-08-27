from typing import Any, List

from fastapi.responses import Response, JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pymongo import MongoClient

from app import crud, models, schemas
from app.api import deps

from app.models import mongo

router = APIRouter()

@router.get("/", response_model=List[mongo.EventModel])
async def read_events(
    db: Session = Depends(deps.get_database),
    #skip: int = 0,
    #limit: int = 100,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve events.
    """
    events = await db["events"].find().to_list(1000)
    return events


@router.post("/", response_model=mongo.EventModel)
async def create_event(
    *,
    db: MongoClient = Depends(deps.get_database),
    event_in: mongo.EventModel = Body(...),
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new event.
    """
    event = jsonable_encoder(event_in)
    new_event = await db["events"].insert_one(event)
    created_event = await db["events"].find_one({"_id": new_event.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_event)


@router.put("/{id}/image", response_model=mongo.EventModel)
def update_image() -> Any:
    pass

@router.put("/{id}/media", response_model=mongo.EventModel)
def update_media() -> Any:
    pass

@router.put("/{id}", response_description="Update a event", response_model=mongo.EventModel)
async def update_event(
    *,
    db: Session = Depends(deps.get_database),
    id: str, 
    event: mongo.UpdateEventModel = Body(...),
    current_user: models.User = Depends(deps.get_current_active_user),
):

    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    event = {k: v for k, v in event.dict().items() if v is not None}

    if len(event) >= 1:
        update_result = await db["events"].update_one({"_id": id}, {"$set": event})

        if update_result.modified_count == 1:
            if (
                updated_event := await db["events"].find_one({"_id": id})
            ) is not None:
                return updated_event

    if (existing_event := await db["events"].find_one({"_id": id})) is not None:
        return existing_event

    raise HTTPException(status_code=404, detail=f"Event {id} not found")

@router.get(
    "/{id}", response_description="Get a single event", response_model=mongo.EventModel
)
async def read_event(
    *,
    db: Session = Depends(deps.get_database),
    id: str
) -> Any:
    """
    Get event by ID.
    """
    if (event := await db["events"].find_one({"_id": id})) is not None:
        return event

    raise HTTPException(status_code=404, detail=f"Event {id} not found")


@router.delete("/{id}", response_description="Delete a events")
async def delete_events(*,
    db: MongoClient = Depends(deps.get_database),    
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user)
    ):

    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    delete_result = await db["events"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Event {id} not found")