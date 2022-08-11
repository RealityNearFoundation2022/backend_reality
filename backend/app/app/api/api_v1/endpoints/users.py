from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, File, UploadFile
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from uuid import uuid4

import os

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email

router = APIRouter()





@router.patch("/image", response_model=schemas.User)
async def upload_image_user(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_user)
    ) -> Any:
    """
    Update image of user.
    """
    user = crud.user.get(db=db, id=current_user.id)
    #if not user:
    #print(file.filename)
    #print(file.write(bytes))
    #print(file.read(bytes))
    contents = file.file.read()

    # print(contents)
    extension = os.path.splitext(file.filename)[1]

    #print(extension)

    # print(extension != ".jpg")

    if extension != ".jpg" and extension != ".png":
        raise HTTPException(
            status_code=400,
            detail="The extension must be jpg or png",
        )

    compress_file = '{}{}'.format(uuid4(), extension)  

    with open('./static/' + compress_file, 'wb') as image:
        image.write(contents)
        image.close()

    path = '/api/v1/static/' + compress_file

    print(user.__dict__)

    user_in = schemas.UserUpdate(
        email = user.email,
        is_active = user.is_active,
        is_superuser= user.is_superuser,
        full_name= user.full_name,
        path=path,
        password=""
    )

    user = crud.user.update(db, db_obj=user, obj_in=user_in)

    # update user data with path

    return user


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    configuration_in = schemas.ConfigurationCreate(location_enabled=0)
    configuration = crud.configuration.create(db, obj_in=configuration_in)

    location_in = schemas.LocationCreate(
        lat = 0,
        lng = 0
    )

    location = crud.location.create(db, obj_in=location_in)

    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    avatar: str = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    if avatar is not None:
        user_in.avatar = avatar
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=schemas.User)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    user = crud.user.create(db, obj_in=user_in)

    configuration_in = schemas.ConfigurationCreate(location_enabled=0, owner_id=user.id)
    configuration = crud.configuration.create(db, obj_in=configuration_in)

    location_in = schemas.LocationCreate(
        lat = 0,
        lng = 0,
        owner_id = user.id
    )

    location = crud.location.create(db, obj_in=location_in)

    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    #if not crud.user.is_superuser(current_user):
    #    raise HTTPException(
    #        status_code=400, detail="The user doesn't have enough privileges"
    #    ) 
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
