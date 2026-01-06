"""
FILE: database.py
PURPOSE: Handles the connection to the SQLite database.

WHY USE THIS STRUCTURE?
1. Separation of Concerns: This file only cares about "connecting". It doesn't care about tables or API routes.
2. Session Management: We use a generator (`get_db`) to ensure the database connection opens and closes cleanly for every request.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# The location of our file-based database. 
# In production, this would be an environment variable (e.g., os.getenv("DATABASE_URL")).
DATABASE_URL = "sqlite:///./notes.db"

# WHY: check_same_thread=False is required for SQLite because it doesn't support
# multi-threading by default. FastAPI is multi-threaded, so we must enable this.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# WHY: SessionLocal acts as a "factory" for new database sessions.
# autocommit=False ensures we explicitly verify data before saving (safer).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models. All database tables will inherit from this.
Base = declarative_base()

def get_db():
    """
    DEPENDENCY INJECTION UTILITY:
    This function is used by FastAPI endpoints to get a database session.
    
    WHY YIELD?
    This is a Python generator.
    1. It opens the session (`db = SessionLocal()`).
    2. It pauses and gives the session to the API endpoint (`yield db`).
    3. When the API endpoint finishes (or fails), it resumes and runs `db.close()`.
    
    This guarantees we never leave "hanging" connections, even if the app crashes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()