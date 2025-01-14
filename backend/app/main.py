from fastapi import FastAPI
from .db import Base, engine
from .routes import users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
def root():
    return {"message": "CFO Assistant API is running!"}
