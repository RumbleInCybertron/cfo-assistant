from fastapi import FastAPI
from app.routes import users, budgets
from app.db import Base, engine
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(budgets.router, prefix="/budgets", tags=["budgets"])

@app.get("/")
def root():
    return {"message": "Welcome to the CFO Assistant API!"}
