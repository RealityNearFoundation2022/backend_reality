from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Notification])
def read_notifications(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve Notifications.
    """
    if crud.user.is_superuser(current_user):
        notifications = crud.notification.get_multi(db, skip=skip, limit=limit)
    else:
        notifications = crud.notification.get_multi_only_pending(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return notifications


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


@router.put("/{id}", response_model=schemas.Notification)
def update_notifications(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    # notification_in: schemas.NotificationUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an Notification.
    """
    notification = crud.notification.get(db=db, id=id)
    
    notification_in = schemas.NotificationUpdate(
        type = notification.type,
        # notification reader
        read=1,
        data=notification.data,
        owner_id=notification.owner_id
    )
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if not crud.user.is_superuser(current_user) and (notification.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    notification = crud.notification.update(db=db, db_obj=notification, obj_in=notification_in)
    return notification



@router.get("/history", response_model=List[schemas.Notification])
def read_notification_history(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get Notifications History Only Readers
    """
    if crud.user.is_superuser(current_user):
        notifications = crud.notification.get_multi(db, skip=skip, limit=limit)
    else:
        notifications = crud.notification.get_multi_reader(db=db, owner_id=current_user.id, skip=skip, limit=limit)
    return notifications

# @router.get("/{id}", response_model=schemas.Item)
# def read_item(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Get item by ID.
#     """
#     item = crud.item.get(db=db, id=id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     return item


@router.delete("/{id}", response_model=schemas.Notification)
def delete_notification(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an notification (only users admin).
    """
    notification = crud.notification.get(db=db, id=id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if not crud.user.is_superuser(current_user) and (notification.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    notification = crud.notification.remove(db=db, id=id)
    return notification
