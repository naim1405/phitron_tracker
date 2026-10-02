from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User
from app.transactions import schemas, service

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/filter", response_model=list[schemas.TransactionResponse])
def filter_transactions(
    type: Optional[str] = None,
    category: Optional[str] = None,
    minimum_amount: Optional[float] = None,
    maximum_amount: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.filter_transactions(current_user.id, db, type, category, minimum_amount, maximum_amount)


@router.post("", response_model=schemas.TransactionResponse, status_code=201)
def create_transaction(
    data: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create_transaction(data, current_user.id, db)


@router.get("", response_model=list[schemas.TransactionResponse])
def get_all_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_all_transactions(current_user.id, db)


@router.get("/{transaction_id}", response_model=schemas.TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_transaction_by_id(transaction_id, current_user.id, db)


@router.put("/{transaction_id}", response_model=schemas.TransactionResponse)
def update_transaction(
    transaction_id: int,
    data: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.update_transaction(transaction_id, data, current_user.id, db)


@router.delete("/{transaction_id}", status_code=200)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service.delete_transaction(transaction_id, current_user.id, db)
    return {"message": "Transaction deleted successfully"}
