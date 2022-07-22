from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


# @router.get("/", response_model=List[schemas.Configuration])
# def read_configuration(
#     db: Session = Depends(deps.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Retrieve configurations.
#     """
#     if crud.user.is_superuser(current_user):
#         configurations = crud.configuration.get_multi(db, skip=skip, limit=limit)
#     else:
#         configurations = crud.configuration.get_multi_by_owner(
#             db=db, owner_id=current_user.id, skip=skip, limit=limit
#         )
#     return configurations


@router.put("/", response_model=schemas.Configuration)
def update_configuration(
    *,
    db: Session = Depends(deps.get_db),
    # id: int,
    configuration_in: schemas.ConfigurationUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an configuration.
    """
    configuration = crud.configuration.get_last(db=db, owner_id=current_user.id)
    if not configuration:
        raise HTTPException(status_code=404, detail="Configuration not found")
    if not crud.user.is_superuser(current_user) and (configuration.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    configuration = crud.configuration.update(db=db, db_obj=configuration, obj_in=configuration_in)
    return configuration


@router.get("/", response_model=schemas.Configuration)
def read_configuration(
    *,
    db: Session = Depends(deps.get_db),
    # id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get Configuration by ID.
    """
    configuration = crud.configuration.get_last(db=db, owner_id=current_user.id)
    if not configuration:
        raise HTTPException(status_code=404, detail="Configuration not found")
    if not crud.user.is_superuser(current_user) and (configuration.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return configuration

