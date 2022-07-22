from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

# ADMIN DATA

def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841

    config = crud.configuration.get_multi_by_owner(db, owner_id=user.id)

    if not config:

        configuration_in = schemas.ConfigurationCreate(
            location_enabled=0,
            owner_id=user.id
        )

        configuration = crud.configuration.create(db, obj_in=configuration_in) # noqa: F841


    location = crud.location.get_last(db, owner_id=user.id)

    if not location:

        location_in = schemas.LocationCreate(
            lng = 0,
            lat = 0,
            owner_id = user.id
        )

        location = crud.location.create(db, obj_in=location_in) # noqa: F841