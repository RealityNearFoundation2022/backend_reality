from .crud_item          import item
from .crud_user          import user
from .crud_contact       import contact
from .crud_report        import report
from .crud_configuration import configuration
from .crud_notification  import notification
from .crud_location      import location
from .crud_couponapp        import coupon, category, redeemed
from .crud_coupon_assign import couponassigned
from .crud_asset         import asset
from .crud_asset_location import asset_location
# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
