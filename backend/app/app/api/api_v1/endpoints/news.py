from typing import Any, List

from fastapi.responses import Response, JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Body, status, File, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

from app.utils import save_image

from app.models import mongo
from pymongo import MongoClient

router = APIRouter()


COLLECTION_NEWS = "news"

formats = [".png", ".jpg"]

@router.get("/", response_model=List[mongo.ListNewModel])
async def read_news(
    db: Session = Depends(deps.get_database),
    #skip: int = 0,
    #limit: int = 100,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve events.
    """
    news = await db[COLLECTION_NEWS].find().to_list(1000)
    return news


@router.post("/", response_model=mongo.NewModel)
async def create_news(
    *,
    db: MongoClient = Depends(deps.get_database),
    new_in: mongo.NewModel = Body(...),
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create news.
    """
    new = jsonable_encoder(new_in)
    new_new = await db[COLLECTION_NEWS].insert_one(new)
    created_new = await db[COLLECTION_NEWS].find_one({"_id": new_new.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_new)


@router.patch("/{id}/image", response_model=mongo.ListNewModel)
async def upload_image(
    *,
    db: MongoClient = Depends(deps.get_database),
    id: str,
    file: UploadFile = File(...),
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add image (portada) to news.
    """
    new = await db[COLLECTION_NEWS].find_one({"_id": id})
    
    if new is None:
        raise HTTPException(status_code=404, detail=f"New {id} not found")

    path = save_image(formats, "news", file)

    new["image"] = path

    update_result = await db[COLLECTION_NEWS].update_one({"_id": id}, {"$set": new})

    if update_result.modified_count == 1:
        if (
            updated_new := await db[COLLECTION_NEWS].find_one({"_id": id})
        ) is not None:
            return updated_new

    raise HTTPException(status_code=400, detail=f"Error Save image {id}")


@router.patch("/{id}/article/{text}")
async def add_article(
    *,
    db: MongoClient = Depends(deps.get_database),
    id: str,
    text: str,
    file: UploadFile = File(...)
) -> Any:
    """
    Add article to new
    """
    new = await db[COLLECTION_NEWS].find_one({"_id": id})
    
    if new is None:
        raise HTTPException(status_code=404, detail=f"New {id} not found")
    
    path = save_image(formats, "news", file)

    d = {"EventNewCreate": new}

    arr = []
    if 'articles' in new:
        arr = new["articles"]
    
    print(text)

    arr.append({
        "data": text,
        "image": path,
    })

    d["EventNewCreate"]["articles"] = arr

    update_result = await db[COLLECTION_NEWS].update_one({"_id": id}, {"$set": d["EventNewCreate"]})

    if update_result.modified_count == 1:
        if (
            updated_new := await db[COLLECTION_NEWS].find_one({"_id": id})
        ) is not None:
            return updated_new

    raise HTTPException(status_code=400, detail=f"Error Save article {id}")



@router.put("/{id}", response_description="Update a new", response_model=mongo.ListNewModel)
async def update_new(
    *,
    db: Session = Depends(deps.get_database),
    id: str,
    new: mongo.UpdateNewModel = Body(...),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an news.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    new = {k: v for k, v in new.dict().items() if v is not None}

    if len(new) >= 1:
        update_result = await db[COLLECTION_NEWS].update_one({"_id": id}, {"$set": new})

        if update_result.modified_count == 1:
            if (
                updated_new := await db[COLLECTION_NEWS].find_one({"_id": id})
            ) is not None:
                return updated_new

    if (existing_new := await db[COLLECTION_NEWS].find_one({"_id": id})) is not None:
        return existing_new

    raise HTTPException(status_code=404, detail=f"New {id} not found")



@router.get(
    "/{id}", response_description="Get a single new", response_model=mongo.ListNewModel
)
async def read_new(
    *,
    db: Session = Depends(deps.get_database),
    id: str
) -> Any:
    """
    Get new by ID.
    """
    if (new := await db[COLLECTION_NEWS].find_one({"_id": id})) is not None:
        return new

    raise HTTPException(status_code=404, detail=f"New {id} not found")


@router.delete("/{id}", response_description="Delete a new")
async def delete_new(*,
    db: MongoClient = Depends(deps.get_database),    
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user)
    ):

    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    delete_result = await db[COLLECTION_NEWS].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Event {id} not found")