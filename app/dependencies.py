from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_sessionmaker


async def get_session() -> AsyncGenerator[AsyncSession]:
    """Yield a database session and close it when the dependency exits."""
    LocalSession = await get_sessionmaker()

    async with LocalSession() as _session:
        yield _session


_AsyncSession = Annotated[AsyncSession, Depends(get_session)]
