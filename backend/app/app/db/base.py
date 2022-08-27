# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.item import Item  # noqa
from app.models.user import User  # noqa
from app.models.contact import Contact  # noqa
from app.models.report import Report
from app.models.location import Location
from app.models.notification import Notification
from app.models.coupon import Coupon, Asset, CouponAssigned