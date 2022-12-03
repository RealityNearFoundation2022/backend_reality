from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from uuid import uuid4


from app.utils import save_image

import os

router = APIRouter()


# @router.get("/", response_model=List[schemas.AssetLocation])
# def read_assets_location(
#     db: Session = Depends(deps.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Retrieve assets.
#     """
#    
#     assets = crud.asset.get_multi(db, skip=skip, limit=limit)
# 
#     return assets


@router.post("/{id}/location", response_model=schemas.Asset)
def create_asset_location(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    asset_in: schemas.AssetLocationCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create location by asset.
    """
    asset_id = crud.asset_location.create_with_asset(db=db, obj_in=asset_in, asset_id=id)
    asset = crud.asset.get(db=db, id=asset_id)
    return asset


@router.put("/{location_id}/location", response_model=schemas.Asset)
def update_asset_location(
    *,
    db: Session = Depends(deps.get_db),
    location_id: int,
    asset_in: schemas.AssetLocationUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an Asset Location.
    """
    asset = crud.asset_location.get(db=db, id=location_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset Location not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    asset_update = crud.asset_location.update(db=db, db_obj=asset, obj_in=asset_in)
    asset = crud.asset.get(db=db, id=asset_update.asset_id)
    return asset


@router.get("/{id}/location", response_model=schemas.Asset)
def read_asset_location(
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


@router.delete("/{location_id}/location", response_model=schemas.Asset)
def delete_asset_location(
    *,
    db: Session = Depends(deps.get_db),
    location_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an Asset.
    """
    asset = crud.asset_location.get(db=db, id=location_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    asset_removed = crud.asset_location.remove(db=db, id=location_id)
    asset = crud.asset.get(db=db, id=asset_removed.asset_id)
    return asset
