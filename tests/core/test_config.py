from __future__ import annotations

from app.core.config import Settings


def test_database_url_converts_postgres_scheme():
    """Verify that postgres URLs use the asyncpg driver."""
    settings = Settings(DATABASE_URL="postgres://user:password@localhost/db")

    assert settings.DATABASE_URL == "postgresql+asyncpg://user:password@localhost/db"


def test_database_url_converts_postgresql_scheme():
    """Verify that postgresql URLs use the asyncpg driver."""
    settings = Settings(DATABASE_URL="postgresql://user:password@localhost/db")

    assert settings.DATABASE_URL == "postgresql+asyncpg://user:password@localhost/db"


def test_database_url_keeps_existing_asyncpg_scheme():
    """Verify that URLs already using asyncpg remain unchanged."""
    settings = Settings(DATABASE_URL="postgresql+asyncpg://user:password@localhost/db")

    assert settings.DATABASE_URL == "postgresql+asyncpg://user:password@localhost/db"


def test_database_url_keeps_non_postgres_url():
    """Verify that non-PostgreSQL URLs retain their original scheme."""
    settings = Settings(DATABASE_URL="sqlite+aiosqlite:///./app.db")

    assert settings.DATABASE_URL == "sqlite+aiosqlite:///./app.db"
