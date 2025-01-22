from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, services, models
from app.services import get_db, get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.BudgetResponse)
def create_budget(budget: schemas.BudgetCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return services.create_budget(db, budget, owner_id=current_user.id)

@router.get("/", response_model=List[schemas.BudgetResponse])
def get_all_budgets(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return services.get_budgets(db, owner_id=current_user.id)

@router.put("/{budget_id}", response_model=schemas.BudgetResponse)
def update_budget(budget_id: int, budget: schemas.BudgetCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    updated_budget = services.update_budget(db, budget_id, budget, owner_id=current_user.id)
    if not updated_budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return updated_budget

@router.delete("/{budget_id}", response_model=schemas.BudgetResponse)
def delete_budget(budget_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    deleted_budget = services.delete_budget(db, budget_id, owner_id=current_user.id)
    if not deleted_budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return deleted_budget
