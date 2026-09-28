from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.config import get_settings

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


Base = declarative_base()


_session = None
_init_lock = asyncio.Lock()


async def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    global _session

    if _session is not None:
        return _session

    async with _init_lock:
        if _session is not None:
            return _session

        engine = create_async_engine(get_settings().DATABASE_URL, echo=True)

        _session = async_sessionmaker(
            bind=engine,
            autoflush=False,
            expire_on_commit=False,
        )

    return _session
