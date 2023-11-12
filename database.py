from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from apps.core.config import settings

async_engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=settings.DEBUG)

SessionLocal = sessionmaker(autocommit=False, bind=async_engine, class_=AsyncSession)

Base = declarative_base()
