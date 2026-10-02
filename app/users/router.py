from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.users import schemas, service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def register(data: schemas.RegisterRequest, db: Session = Depends(get_db)):
    return service.register_user(data, db)


@router.post("/login", response_model=schemas.TokenResponse)
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    token = service.login_user(data, db)
    return {"access_token": token, "token_type": "bearer"}
