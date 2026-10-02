from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Transaction
from app.transactions.schemas import TransactionCreate, TransactionUpdate


def create_transaction(data: TransactionCreate, owner_id: int, db: Session) -> Transaction:
    transaction = Transaction(**data.model_dump(), owner_id=owner_id)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def get_all_transactions(owner_id: int, db: Session) -> list[Transaction]:
    return db.query(Transaction).filter(Transaction.owner_id == owner_id).all()


def get_transaction_by_id(transaction_id: int, owner_id: int, db: Session) -> Transaction:
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.owner_id == owner_id,
    ).first()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction


def update_transaction(transaction_id: int, data: TransactionUpdate, owner_id: int, db: Session) -> Transaction:
    transaction = get_transaction_by_id(transaction_id, owner_id, db)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(transaction, field, value)
    db.commit()
    db.refresh(transaction)
    return transaction


def delete_transaction(transaction_id: int, owner_id: int, db: Session) -> None:
    transaction = get_transaction_by_id(transaction_id, owner_id, db)
    db.delete(transaction)
    db.commit()


def filter_transactions(
    owner_id: int,
    db: Session,
    type: Optional[str] = None,
    category: Optional[str] = None,
    minimum_amount: Optional[float] = None,
    maximum_amount: Optional[float] = None,
) -> list[Transaction]:
    query = db.query(Transaction).filter(Transaction.owner_id == owner_id)

    if type:
        query = query.filter(Transaction.type == type)
    if category:
        query = query.filter(Transaction.category == category)
    if minimum_amount is not None:
        query = query.filter(Transaction.amount >= minimum_amount)
    if maximum_amount is not None:
        query = query.filter(Transaction.amount <= maximum_amount)

    return query.all()
