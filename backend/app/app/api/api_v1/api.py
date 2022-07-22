from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, utils, contacts, location, notifications, reports, configuration

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
api_router.include_router(location.router, prefix="/location", tags=["location"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(configuration.router, prefix="/configuration", tags=["configuration"])
