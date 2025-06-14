from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class BudgetBase(BaseModel):
    name: str
    amount: float

class BudgetCreate(BudgetBase):
    pass

class BudgetResponse(BudgetBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    amount: float
    category_id: int
    date: Optional[datetime] = None

class TransactionCreate(TransactionBase):
    budget_id: int

class TransactionResponse(TransactionBase):
    id: int
    budget_id: int

    class Config:
        from_attributes = True

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None