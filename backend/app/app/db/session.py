from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

print(settings.MONGOALCHEMY_DATABASE_URI)

#engine2 = create_engine("mongodb:///?mongo=mongo&;Port=27017&Database=test&User=root&Password=example", pool_pre_ping=True)
#SessionLocalMongo = sessionmaker(autocommit=False, autoflush=False, bind=engine2)

