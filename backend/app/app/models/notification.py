from sqlalchemy.ext.mutable import Mutable

class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()

# -----------------------

from typing import TYPE_CHECKING


from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from sqlalchemy.types import TypeDecorator, VARCHAR

import json
# import sqlalchemy as sqla
# from sqlalchemy.ext import mutable


from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class JSONEncodedDict(TypeDecorator):
    "Represents an immutable structure as a json-encoded string."

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class Notification(Base):
    id = Column(Integer, primary_key=True, index=True)
    read = Column(Integer, default=0)
    type = Column(String, nullable=False)
    data = Column(MutableDict.as_mutable(JSONEncodedDict))
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="notifications")
