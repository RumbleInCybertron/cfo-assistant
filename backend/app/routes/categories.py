# app/routes/categories.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Category, Transaction
from app.schemas import CategoryResponse, CategoryCreate
from app.services import get_db, get_current_user

router = APIRouter()

@router.get("/", response_model=list[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    categories = db.query(Category).filter(
        (Category.user_id == None) | (Category.user_id == current_user["id"])
    ).all()
    return categories

@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    existing = db.query(Category).filter(
        Category.name == category.name,
        (Category.user_id == None) | (Category.user_id == current_user["id"])
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists.")
    
    new_category = Category(name=category.name, is_custom=True, user_id=current_user["id"])
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/{category_id}/transactions", response_model=list[TransactionResponse])
def get_transactions_by_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    transactions = db.query(Transaction).filter(
        Transaction.category_id == category_id
    ).all()
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this category.")
    return transactions
