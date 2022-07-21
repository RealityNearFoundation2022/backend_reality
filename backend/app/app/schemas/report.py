from typing import Optional

from pydantic import BaseModel


# Shared properties
class ReportBase(BaseModel):
    category: str
    title: str
    description: str
    status: int
    image: str



# Properties to receive on Report creation
class ReportCreate(ReportBase):
    pass


# Properties to receive on Report update
class ReportUpdate(ReportBase):
    pass


# Properties shared by models stored in DB
class ReportInDBBase(ReportBase):
    id: int
    category: str
    title: str
    description: str
    status: int
    image: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Report(ReportInDBBase):
    pass


# Properties properties stored in DB
class ReportInDB(ReportInDBBase):
    pass
