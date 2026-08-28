import os

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.database import Base, DATABASE_URL, engine, SessionLocal


def _async_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    if url.startswith("postgresql://"):
        return url.replace(
            "postgresql://",
            "postgresql+asyncpg://",
            1,
        )

    if url.startswith("sqlite:///"):
        path = url[len("sqlite:///"):]
        return f"sqlite+aiosqlite:///{path}"

    return url


ASYNC_DATABASE_URL = _async_database_url(DATABASE_URL)

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session


__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "async_engine",
    "AsyncSessionLocal",
    "get_async_db",
]
