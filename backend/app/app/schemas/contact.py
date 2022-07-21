from typing import Optional

from pydantic import BaseModel


# Shared properties
class ContactBase(BaseModel):
    pending: int = 0 # 0 = pending | 1 = aproved
    contact_id: int
    locked: int 

# Properties to receive on Contact creation
class ContactCreate(BaseModel):
    contact_id: int

# Properties to receive on Contact update
class ContactUpdate(BaseModel):
    approved: int

class ContactLocked(BaseModel):
    locked: int

# Properties shared by models stored in DB
class ContactInDBBase(ContactBase):
    id: int
    pending: int
    contact_id: int
    owner_id: int
    locked: int

    class Config:
        orm_mode = True


# Properties to return to client
class Contact(ContactInDBBase):
    pass


# Properties properties stored in DB
class ContactInDB(ContactInDBBase):
    pass
