from typing import Optional, Any

from pydantic import BaseModel


# Shared properties
class NotificationBase(BaseModel):
    type: str
    read: int
    data: Any = None



# Properties to receive on Notification creation
class NotificationCreate(NotificationBase):
    owner_id: int


# Properties to receive on Notification update
class NotificationUpdate(NotificationBase):
    pass


# Properties shared by models stored in DB
class NotificationInDBBase(NotificationBase):
    id: int
    type: str
    read: int
    data: Any = None
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Notification(NotificationInDBBase):
    pass


# Properties properties stored in DB
class NotificationInDB(NotificationInDBBase):
    pass
