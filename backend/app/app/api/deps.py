from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal#, SessionLocalMongo

import motor.motor_asyncio

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_database():
    #from pymongo import MongoClient
    #import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
                         #mongodb+srv://username:password@mflix-m5hjq.mongodb.net/test?retryWrites=true
    CONNECTION_STRING ="mongodb://root:example@mongo:27017" #"mongodb://root:example@mongo.mongodb.net/myFirstDatabase?retryWrites=true"
    client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING)
    db = client.test
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    #from pymongo import MongoClient
    #client = MongoClient(CONNECTION_STRING)
    #client = MongoClient(host="mongo", port=27017,username="root",password="example")
    # Create the database for our example (we will use the same database throughout the tutorial
    return db

# def get_db_mongo() -> Generator:
#     try:
#         db = SessionLocalMongo()
#         yield db
#     finally:
#         db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
