from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

from app.database import db

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(autouse=True)
async def reset_singleton():
    """`_session` and `_init_lock` are module-level globals -- reset them
    before and after every test so tests can't leak state into each other.
    """
    db._session = None
    db._init_lock = asyncio.Lock()
    yield
    db._session = None


# ---------------------------------------------------------------------------
# The scenario get_sessionmaker() actually promises to handle: many
# coroutines on the SAME event loop (e.g. concurrent request handlers
# in FastAPI) racing to initialize the sessionmaker.
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_concurrent_coroutines_create_engine_exactly_once():
    with patch(
        "app.database.db.create_async_engine", return_value="fake-engine"
    ) as mock_create:
        results = await asyncio.gather(
            *[db.get_sessionmaker() for _ in range(50)],
        )

    assert mock_create.call_count == 1
    first = results[0]
    assert all(r is first for r in results)
    assert db._session is first


@pytest.mark.asyncio
async def test_concurrent_coroutines_return_a_usable_sessionmaker(postgres_url: str):
    fake_settings = SimpleNamespace(DATABASE_URL=postgres_url)

    with patch("app.database.db.get_settings", return_value=fake_settings):
        results = await asyncio.gather(
            *[db.get_sessionmaker() for _ in range(20)],
        )

    first = results[0]
    assert all(r is first for r in results)

    async with first() as session:
        assert session is not None


@pytest.mark.asyncio
async def test_get_sessionmaker_talks_to_real_postgres(sessionmaker: AsyncSession):

    import sqlalchemy

    async with sessionmaker() as session:  # pyright: ignore[reportCallIssue]
        result = await session.execute(sqlalchemy.text("select version()"))
        version = result.scalar()

    assert "PostgreSQL" in version
