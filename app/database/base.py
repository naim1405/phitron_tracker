from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

db_url = settings.database_url.replace("postgresql://", "postgresql+psycopg2://", 1)
engine = create_engine(db_url)


class Base(DeclarativeBase):
    pass
