from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from uuid import uuid4

import os

router = APIRouter()


@router.get("/", response_model=List[schemas.Asset])
def read_assets(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve assets.
    """
   
    assets = crud.asset.get_multi(db, skip=skip, limit=limit)

    return assets


@router.post("/", response_model=schemas.Asset)
def create_asset(
    *,
    db: Session = Depends(deps.get_db),
    asset_in: schemas.AssetCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new asset.
    """
    asset = crud.asset.create(db=db, obj_in=asset_in)
    return asset


@router.patch("/{id}/image", response_model=schemas.Asset)
async def upload_3d_asset(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_user)
    ) -> Any:
    """
    Update image of user.
    """
    asset = crud.asset.get(db=db, id=id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    user = crud.user.get(db=db, id=current_user.id)
    #if not user:
    #print(file.filename)
    #print(file.write(bytes))
    #print(file.read(bytes))
    contents = file.file.read()

    # print(contents)
    extension = os.path.splitext(file.filename)[1]

    #print(extension)

    # print(extension != ".jpg")

    if extension != ".glb":
        raise HTTPException(
            status_code=400,
            detail="The extension must be .glb",
        )

    compress_file = '{}{}'.format(uuid4(), extension)  

    with open('./static/assets/' + compress_file, 'wb') as image:
        image.write(contents)
        image.close()

    path = '/api/v1/static/assets/' + compress_file

    # print(user.__dict__)

    asset_in = schemas.AssetUpdate(
        name = asset.name,
        path = path
    )

    asset = crud.asset.update(db, db_obj=asset, obj_in=asset_in)

    return asset

@router.put("/{id}", response_model=schemas.Asset)
def update_asset(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    asset_in: schemas.AssetUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an Asset.
    """
    asset = crud.asset.get(db=db, id=id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    asset = crud.asset.update(db=db, db_obj=asset, obj_in=asset_in)
    return asset


@router.get("/{id}", response_model=schemas.Asset)
def read_asset(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get Asset by ID.
    """
    asset = crud.asset.get(db=db, id=id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.delete("/{id}", response_model=schemas.Asset)
def delete_asset(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an Asset.
    """
    asset = crud.asset.get(db=db, id=id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    asset = crud.asset.remove(db=db, id=id)
    return asset
