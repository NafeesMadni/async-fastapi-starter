"""
Run tests against a REAL PostgreSQL server without having one already
running anywhere (no Docker, no system install, no root/admin rights).

    uv add --dev pytest-asyncio pgembed

pgembed ships actual postgres binaries as a pip wheel and boots a
disposable instance in a temp directory -- the same convenience SQLite's
":memory:" gives you, but it's genuinely PostgreSQL underneath (real
dialect, real types, SERIAL/RETURNING/JSONB, etc.), so your Alembic
migrations and Postgres-specific SQL are exercised for real.
"""

from __future__ import annotations

import tempfile
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any
from unittest.mock import patch

import pgembed
import pytest
import pytest_asyncio

from app.database import db

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Generator

    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


@pytest.fixture(scope="session")
def postgres_url() -> Generator[str]:
    """Boots one embedded Postgres for the whole test session (~0.5s)."""

    pg = pgembed.get_server(tempfile.mkdtemp())  # type: ignore
    url = pg.get_uri().replace("postgresql://", "postgresql+asyncpg://", 1)
    yield url
    pg.cleanup()


@pytest_asyncio.fixture
async def sessionmaker(
    postgres_url: str,
) -> AsyncGenerator[async_sessionmaker[AsyncSession], Any]:
    """get_sessionmaker(), pointed at the embedded Postgres instead of
    whatever app.config.get_settings() would normally return, with the
    schema created fresh for this test."""

    fake_settings = SimpleNamespace(DATABASE_URL=postgres_url)

    with patch("app.database.db.get_settings", return_value=fake_settings):
        sm = await db.get_sessionmaker()

    async with sm.kw["bind"].begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)

    yield sm

    async with sm.kw["bind"].begin() as conn:
        await conn.run_sync(db.Base.metadata.drop_all)
