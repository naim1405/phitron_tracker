from sqlalchemy.orm import Session, sessionmaker

from .base import engine

SessionLocal = sessionmaker(bind=engine)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
