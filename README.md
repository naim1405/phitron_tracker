## Run the API

Copy `.env.example` to `.env` and set the database URL and JWT secrets. Then run:

```bash
uv run python main.py
```

The health check is available at `http://127.0.0.1:8000/health`.

## Migrations

```bash
# Apply all pending migrations
uv run alembic upgrade head

# Generate a new migration after model changes
uv run alembic revision --autogenerate -m "your message"

# Rollback one migration
uv run alembic downgrade -1

# Check current migration state
uv run alembic current
```
