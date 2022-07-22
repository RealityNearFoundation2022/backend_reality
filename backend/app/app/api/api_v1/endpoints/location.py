from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


# @router.get("/", response_model=List[schemas.Item])
# def read_items(
#     db: Session = Depends(deps.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Retrieve items.
#     """
#     if crud.user.is_superuser(current_user):
#         items = crud.item.get_multi(db, skip=skip, limit=limit)
#     else:
#         items = crud.item.get_multi_by_owner(
#             db=db, owner_id=current_user.id, skip=skip, limit=limit
#         )
#     return items


# @router.post("/", response_model=schemas.Item)
# def create_item(
#     *,
#     db: Session = Depends(deps.get_db),
#     item_in: schemas.ItemCreate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Create new item.
#     """
#     item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
#     return item


@router.put("/", response_model=schemas.Location)
def update_location(
    *,
    db: Session = Depends(deps.get_db),
    location_in: schemas.LocationUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an location.
    """
    location = crud.location.get_last(db=db, owner_id=current_user.id)
    if not location:
        raise HTTPException(status_code=404, detail="location not found")
    if not crud.user.is_superuser(current_user) and (location.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    location = crud.location.update(db=db, db_obj=location, obj_in=location_in)
    return location


@router.get("/", response_model=schemas.Location)
def read_location(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get location by ID.
    """
    location = crud.location.get_last(db=db, owner_id=current_user.id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    if not crud.user.is_superuser(current_user) and (location.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return location


@router.get("/{id}/friend", response_model=schemas.Location)
def read_location_by_friend(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get location by friend.
    """

    # is friend
    contact = crud.contact.get_by_owner_and_contact(db, owner_id=current_user.id, contact_id=id)

    if not contact:
        raise HTTPException(status_code=404, detail="Friend not found")

    # config friend data
    config_contact = crud.configuration.get_multi_by_owner(db, owner_id=id)

    if not config_contact:
        raise HTTPException(status_code=404, detail="Not Config Friend")


    if not config_contact[0].location_enabled:
        raise HTTPException(status_code=404, detail="Location not enabled")

    location = crud.location.get_last(db=db, owner_id=id)

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    if not crud.user.is_superuser(current_user) and (location.owner_id != id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return location


# @router.delete("/{id}", response_model=schemas.Item)
# def delete_item(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Delete an item.
#     """
#     item = crud.item.get(db=db, id=id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     item = crud.item.remove(db=db, id=id)
#     return item
