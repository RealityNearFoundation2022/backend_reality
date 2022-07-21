from typing import Any, Dict, List

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
        contacts = crud.contact.get_multi_by_owner_and_relation_accepted(
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

    # valid if contact exists
    contact_data = crud.user.get(db=db, id=contact_in.contact_id)
    if not contact_data:
        raise HTTPException(status_code=404, detail="contact not found")

    if current_user.id == contact_in.contact_id:
        raise HTTPException(status_code=404, detail="can't add yourself how friend")


    contact = crud.contact.get_multi_by_owner_and_contact(db=db, contact_id=contact_in.contact_id, owner_id=current_user.id)

    if contact:
        raise HTTPException(status_code=404, detail="contact exits")

    # create contact in db
    contact = crud.contact.create_with_owner(db=db, obj_in=contact_in, owner_id=current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="contact not save, try again")
    

    # notification --> esto debe salir a eventos | create notification in db
    notification_in = schemas.NotificationCreate(
        type="friend",
        read=0,
        data={
            "contact_id": current_user.id,
            "username": current_user.full_name
        },
        owner_id=contact_in.contact_id
    )

    notification = crud.notification.create(db=db, obj_in=notification_in)
    return contact


@router.put("/{id}/approved", response_model=schemas.Contact)
def update_contact(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    # contact_in: schemas.ContactUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update Approve an contact.
    """
    contact = crud.contact.get(db=db, id=id)
    if not contact:
        raise HTTPException(status_code=404, detail="contact not found")
    if not crud.user.is_superuser(current_user) and (contact.contact_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    # if (contact.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="You don't update this contact")
    
    # approved 0 (pendiente) | 1 (aprovado)
    contact_in = schemas.ContactUpdate(
        approved = 1
    )

    contact = crud.contact.update_pending(db=db, db_obj=contact, obj_in=contact_in)
    return contact

@router.put("/{id}/locked", response_model=schemas.Contact)
def update_contact_lock(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    contact_in: schemas.ContactLocked,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update Lock an contact.
    """
    contact = crud.contact.get(db=db, id=id)
    if not contact:
        raise HTTPException(status_code=404, detail="contact not found")
    if not crud.user.is_superuser(current_user) and (contact.contact_id != current_user.id):
        if (contact.owner_id != current_user.id): 
            raise HTTPException(status_code=400, detail="Not enough permissions")
    
    # if (contact.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="You don't update this contact")

    contact = crud.contact.update(db=db, db_obj=contact, obj_in=contact_in)
    return contact



@router.get("/pending", response_model=List[schemas.Contact])
def read_contacts_pending(
    *,
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
        contacts = crud.contact.get_multi_by_owner_and_relation_pending(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return contacts


@router.delete("/{id}", response_model=schemas.Contact)
def remove_contact(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove an contact.
    """
    contact = crud.contact.get(db=db, id=id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    if not crud.user.is_superuser(current_user) and (contact.owner_id != current_user.id):
        if (contact.contact_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")
    contact = crud.contact.remove(db=db, id=id)
    return contact
