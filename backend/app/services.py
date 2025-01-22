from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.models import User
from app.db import SessionLocal
from sqlalchemy.orm import Session
from . import models, schemas

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Set up the password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    """Provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Retrieve the currently authenticated user from the JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user

def get_password_hash(password: str) -> str:
    """Hash a plain password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_budget(db: Session, budget: schemas.BudgetCreate, owner_id: int):
    db_budget = models.Budget(**budget.dict(), owner_id=owner_id)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def get_budgets(db: Session, owner_id: int):
    return db.query(models.Budget).filter(models.Budget.owner_id == owner_id).all()

def update_budget(db: Session, budget_id: int, budget: schemas.BudgetCreate, owner_id: int):
    db_budget = db.query(models.Budget).filter(models.Budget.id == budget_id, models.Budget.owner_id == owner_id).first()
    if db_budget:
        for key, value in budget.dict().items():
            setattr(db_budget, key, value)
        db.commit()
        db.refresh(db_budget)
    return db_budget

def delete_budget(db: Session, budget_id: int, owner_id: int):
    db_budget = db.query(models.Budget).filter(models.Budget.id == budget_id, models.Budget.owner_id == owner_id).first()
    if db_budget:
        db.delete(db_budget)
        db.commit()
    return db_budget