from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate

from sqlalchemy import or_


class CRUDContact(CRUDBase[Contact, ContactCreate, ContactUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: ContactCreate, owner_id: int
    ) -> Contact:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner_and_contact(self, db: Session, owner_id: int, contact_id: int) -> Contact:
        return db.query(self.model).filter(Contact.owner_id == owner_id, Contact.contact_id == contact_id).first()

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Contact]:
        return (
            db.query(self.model)
            .filter(Contact.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_multi_by_owner_and_relation(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Contact]:
        return (
            db.query(self.model)
            .filter(
                or_(
                    Contact.owner_id == owner_id, 
                    Contact.contact_id == owner_id
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_owner_and_relation_pending(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Contact]:
        return (
            db.query(self.model)
            .filter(
                or_(
                    Contact.owner_id == owner_id, 
                    Contact.contact_id == owner_id
                ),
                # 0 = pending  
                Contact.pending == 0
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_multi_by_owner_and_relation_accepted(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    )-> List[Contact]:
        return (
            db.query(self.model)
            .filter(
                or_(
                    Contact.owner_id == owner_id, 
                    Contact.contact_id == owner_id
                ),
                # 0 = pending  
                Contact.pending == 1
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update_pending(
        self,
        db: Session,
        *,
        db_obj: Contact,
        obj_in: ContactUpdate
    ) -> Contact:
        # obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        # for field in obj_data:
        #     if field in update_data:
        setattr(db_obj, 'pending', update_data['approved'])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


contact = CRUDContact(Contact)
