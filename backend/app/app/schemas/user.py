from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    username: Optional[str] = None
    path: Optional[str] = None
    avatar: Optional[str] = None
    is_invited: Optional[str] = None
#    reports: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    # password: Optional[str] = None
    pass


class UserInDBBase(UserBase):
    id: Optional[int] = None
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    updated_at: datetime


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
    updated_at: datetime = datetime.utcnow()
