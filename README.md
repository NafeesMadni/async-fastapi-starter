# Async FastAPI Starter

A small, async-first FastAPI starter with SQLAlchemy 2.x, Alembic, and PostgreSQL. It includes a concurrency-guarded async session factory and keeps the app structure intentionally lean.

## Stack

- FastAPI
- SQLAlchemy async ORM with `asyncpg`
- Alembic async migrations
- PostgreSQL, local or hosted (including Supabase)
- Pydantic Settings for environment-based configuration
- `fastapi-redis-sdk` is installed; Redis lifespan and features are not wired up yet
- Celery and Pydantic Logfire are future integration points

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL for local development, or a hosted PostgreSQL connection string

## Quick start

```bash
git clone <your-repository-url>
cd <repository-directory>
uv sync
cp `.env.example` .env
```

Set `DATABASE_URL` in `.env`:

```dotenv
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/app_db
```

For Supabase, use a connection string from the project's **Connect** dialog. The settings loader accepts `postgres://` and `postgresql://` URLs and converts them to the `asyncpg` dialect. Keep credentials out of source control, and URL-encode special characters in passwords when required.

Apply migrations and start the development server:

```bash
uv run alembic upgrade head
uv run fastapi dev app/main.py
```

The API is available at `http://127.0.0.1:8000`; interactive documentation is at `/docs`.

## Included endpoints

- `GET /health` — basic health response
- `GET /user` — example user query

## Database workflow

Create a migration after changing SQLAlchemy models:

```bash
uv run alembic revision --autogenerate -m "describe the change"
```

Review the generated migration, then apply it:

```bash
uv run alembic upgrade head
```

The async engine and session factory are initialized once per worker process. A lock guards concurrent initialization, and each request receives its own `AsyncSession`; do not share a session across concurrent tasks.

## Tests

The database tests use `pgembed` to run a temporary real PostgreSQL instance:

```bash
uv run pytest
```

## Project structure

```text
app/
  api/v1/
  core/
  database/
migrations/
tests/
```

## Planned integrations

- Redis connection lifecycle and caching with `fastapi-redis-sdk`, composed with the app lifespan as described in the [lifespan-wrapping guide](https://redis.github.io/fastapi-redis-sdk/guide/architecture/#lifespan-wrapping)
- Celery for background jobs
- Pydantic Logfire for tracing and observability
