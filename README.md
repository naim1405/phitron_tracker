## Run the API

Copy `.env.example` to `.env` and set the database URL and JWT secrets. Then run:

```bash
uv run python main.py
```

The health check is available at `http://127.0.0.1:8000/health`.
