"""
Database
"""

from typing import AsyncGenerator, Any

from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from constants import DB_CONN
from admin import init_admin


engine = create_async_engine(DB_CONN, echo=False, future=True)


async def init_database() -> None:
    """Initialise db"""
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

    async with async_sessionmaker(engine, class_=AsyncSession)() as session:
        await init_admin(session)


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    """Yields db session"""
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
