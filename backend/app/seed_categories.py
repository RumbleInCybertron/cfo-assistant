# app/seed_categories.py

from sqlalchemy.orm import Session
from app.db import engine, SessionLocal
from app.models import Category

# Define the predefined categories
PREDEFINED_CATEGORIES = [
    "Food",
    "Transportation",
    "Rent",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Savings",
    "Miscellaneous",
]

def seed_categories():
    session = Session(bind=engine)
    try:
        for category_name in PREDEFINED_CATEGORIES:
            # Check if category already exists
            existing_category = session.query(Category).filter_by(name=category_name).first()
            if not existing_category:
                category = Category(name=category_name, is_custom=False)
                session.add(category)
        
        session.commit()
        print("Categories seeded successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error seeding categories: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_categories()

