from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.utils import create_access_token, hash_password, verify_password
from app.models import User
from app.users.schemas import LoginRequest, RegisterRequest


def register_user(data: RegisterRequest, db: Session) -> User:
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(data: LoginRequest, db: Session) -> str:
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return create_access_token({"sub": str(user.id)})
