from fastapi import FastAPI

from app.config import settings
from app.users import router as auth_router

app = FastAPI(title=settings.app_name)

app.include_router(auth_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
