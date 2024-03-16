from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import mysql_settings

Base = declarative_base()
AsyncDBSessionLocal: Optional[AsyncSession] = None
db_engine: Optional[AsyncEngine] = None


async_engine = create_async_engine(mysql_settings.MYSQL_URI, echo=False, future=True)

local_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


async def async_get_db() -> AsyncSession:
    async_session = local_session
    async with async_session() as db:
        yield db
        await db.commit()

