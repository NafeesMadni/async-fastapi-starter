from __future__ import annotations

from app.core.config import Settings


def test_database_url_converts_postgres_scheme():
    settings = Settings(DATABASE_URL="postgres://user:password@localhost/db")

    assert settings.DATABASE_URL == "postgresql+asyncpg://user:password@localhost/db"


def test_database_url_converts_postgresql_scheme():
    settings = Settings(DATABASE_URL="postgresql://user:password@localhost/db")

    assert settings.DATABASE_URL == "postgresql+asyncpg://user:password@localhost/db"


def test_database_url_keeps_existing_asyncpg_scheme():
    settings = Settings(DATABASE_URL="postgresql+asyncpg://user:password@localhost/db")

    assert settings.DATABASE_URL == "postgresql+asyncpg://user:password@localhost/db"


def test_database_url_keeps_non_postgres_url():
    settings = Settings(DATABASE_URL="sqlite+aiosqlite:///./app.db")

    assert settings.DATABASE_URL == "sqlite+aiosqlite:///./app.db"
