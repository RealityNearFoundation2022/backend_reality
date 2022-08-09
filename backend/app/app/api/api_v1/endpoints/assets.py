from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

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
    asset = crud.Asset.get(db=db, id=id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if not crud.user.is_superuser(current_user) and (asset.owner_id != current_user.id):
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
    if not crud.user.is_superuser(current_user) and (asset.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
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
    if not crud.user.is_superuser(current_user) and (asset.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    asset = crud.asset.remove(db=db, id=id)
    return asset
