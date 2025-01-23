from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import TransactionCreate, TransactionResponse, TransactionUpdate
from app.services import (
    get_db,
    get_current_user, 
    create_transaction as create_transaction_service, 
    get_transactions_by_budget,
    get_transaction_by_id,
    update_transaction as update_transaction_service,
    delete_transaction as delete_transaction_service,
)
from app.models import Transaction

router = APIRouter()

@router.post("/", response_model=TransactionResponse)
def create_transaction_route(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return create_transaction_service(db, transaction)


@router.get("/{budget_id}", response_model=list[TransactionResponse])
def get_transactions(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    transactions = db.query(Transaction).filter(Transaction.budget_id == budget_id).all()
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this budget.")
    return transactions


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction_route(
    transaction_id: int,
    transaction_data: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return update_transaction_service(db, transaction_id, transaction_data)


@router.delete("/{transaction_id}")
def delete_transaction_route(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return delete_transaction_service(db, transaction_id)
