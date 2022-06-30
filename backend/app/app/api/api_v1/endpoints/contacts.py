from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Contact])
def read_contacts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve contacts.
    """
    if crud.user.is_superuser(current_user):
        contacts = crud.contact.get_multi(db, skip=skip, limit=limit)
    else:
        contacts = crud.contact.get_multi_by_owner_and_relation(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return contacts


@router.post("/", response_model=schemas.Contact)
def add_contact(
    *,
    db: Session = Depends(deps.get_db),
    contact_in: schemas.ContactCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    add new contact.
    """
    contact = crud.contact.create_with_owner(db=db, obj_in=contact_in, owner_id=current_user.id)
    return contact


@router.put("/{id}", response_model=schemas.Contact)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    contact_in: schemas.ContactUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an contact.
    """
    contact = crud.contact.get(db=db, id=id)
    if not contact:
        raise HTTPException(status_code=404, detail="contact not found")
    if not crud.user.is_superuser(current_user) and (contact.contact_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    # if (contact.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="You don't update this contact")
    
    # aproved 0(pendiente) | 1 (aprovado) | 2 (cancelado)
    contact = crud.contact.update(db=db, db_obj=contact, obj_in=contact_in)
    return contact


@router.get("/{id}", response_model=schemas.Contact)
def read_contact(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get contact by ID.
    """
    contact = crud.contact.get(db=db, id=id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    if not crud.user.is_superuser(current_user) and (contact.owner_id != current_user.id):
        if (contact.contact_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")    
    return contact


# @router.delete("/{id}", response_model=schemas.Item)
# def remove_contact(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Remove an contact.
#     """
#     item = crud.item.get(db=db, id=id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     item = crud.item.remove(db=db, id=id)
#     return item
