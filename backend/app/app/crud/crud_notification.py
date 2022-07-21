from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate


class CRUDNotification(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: NotificationCreate, owner_id: int
    ) -> Notification:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Notification]:
        return (
            db.query(self.model)
            .filter(Notification.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_multi_reader(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Notification]:
        return (
            db.query(self.model)
            .filter(Notification.owner_id == owner_id, Notification.read != 0)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_only_pending(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Notification]:
        return (
            db.query(self.model)
            .filter(Notification.owner_id == owner_id, Notification.read != 1)
            .offset(skip)
            .limit(limit)
            .all()
        )


notification = CRUDNotification(Notification)
