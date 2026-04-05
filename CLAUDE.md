# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

**Docker (recommended):**
```bash
docker-compose up --build
```
App runs at `http://localhost:8000`. Swagger UI at `http://localhost:8000/docs`.

**Local development** (requires a running PostgreSQL on port 5432):
```bash
pip install -r requirements.txt
cd app
uvicorn main:app --reload
```

**Database connection** defaults to `postgresql+asyncpg://postgres:postgres@localhost:5432/app_db`. Override via `DATABASE_URL` env var.

## Architecture

The app lives entirely under `app/` and is run with `app/` as the working directory, so all imports are relative to that directory (e.g., `from core.database import ...`, not `from app.core.database import ...`).

```
app/
  main.py              # FastAPI app, startup event drops+recreates all tables
  core/
    database.py        # Async SQLAlchemy engine, Base, get_db dependency
    auth.py            # JWT creation/verification, bcrypt hashing, OAuth client secret generation
  models/              # SQLAlchemy ORM models (User, OAuthClient, OAuthToken)
  schemas/             # Pydantic v2 request/response schemas
  repositories/
    user_repo.py       # Data access layer (UserRepository static methods)
  services/
    auth_service.py    # Business logic layer, delegates to UserRepository
  api/v1/endpoints/
    auth.py            # /auth/register and /auth/login routes
```

### Request flow
`endpoint → service → repository → ORM model`

### Key design notes
- **Startup drops and recreates all tables** (`main.py:24–27`). This is intentional for development but means all data is lost on every restart.
- **Double password hashing bug**: `auth_service.register_user` hashes the password before passing it to `UserRepository.create`, which hashes it again (`user_repo.py:15`). Fix is to remove the hash call in one layer.
- **`save_access_token` is broken**: `user_repo.py:78,83` calls `access_token.fresh_token` on a plain `str`. The `Token` schema also lacks a `refresh_token` field. This flow is in-progress/not functional.
- All primary keys use `UUID` (PostgreSQL `uuid` type via `asyncpg`).
- JWT tokens embed `sub` (user UUID) and `client_id` (OAuthClient UUID). `SECRET_KEY` is hardcoded — move to env var before any production use.

## Database

PostgreSQL 15 via Docker Compose. Credentials: `postgres/postgres`, database: `app_db`, port `5432`.

All models must be imported in `main.py` before `Base.metadata.create_all` runs, or their tables won't be created.
