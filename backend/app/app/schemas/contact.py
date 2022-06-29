from typing import Optional

from pydantic import BaseModel


# Shared properties
class ContactBase(BaseModel):
    pending: int
    contact_id: int

# Properties to receive on Contact creation
class ContactCreate(ContactBase):
    pass


# Properties to receive on Contact update
class ContactUpdate(ContactBase):
    pass


# Properties shared by models stored in DB
class ContactInDBBase(ContactBase):
    id: int
    pending: int
    contact_id: int
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Contact(ContactInDBBase):
    pass


# Properties properties stored in DB
class ContactInDB(ContactInDBBase):
    pass
