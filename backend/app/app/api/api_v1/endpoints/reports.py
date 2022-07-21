from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Report])
def read_reports(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve reports.
    """
    if crud.user.is_superuser(current_user):
        reports = crud.report.get_multi(db, skip=skip, limit=limit)
    else:
        reports = crud.report.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return reports


@router.post("/", response_model=schemas.Report)
def create_report(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.ReportCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new report.
    """
    item = crud.report.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    return item


# @router.put("/{id}", response_model=schemas.Item)
# def update_item(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     item_in: schemas.ItemUpdate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update an item.
#     """
#     item = crud.item.get(db=db, id=id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     item = crud.item.update(db=db, db_obj=item, obj_in=item_in)
#     return item


@router.get("/{id}", response_model=schemas.Report)
def read_report(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get  by ID.
    """
    report = crud.report.get(db=db, id=id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if not crud.user.is_superuser(current_user) and (report.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return report


# @router.delete("/{id}", response_model=schemas.Item)
# def delete_itemitem(
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
