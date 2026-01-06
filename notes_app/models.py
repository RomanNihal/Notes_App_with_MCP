"""
FILE: models.py
PURPOSE: Defines the structure (Schema) of our database tables.

WHY USE THE DOT (.) IMPORT?
> from .database import Base

The dot (.) represents a 'Relative Import'. 
It tells Python: "Look for the database.py file inside the SAME PACKAGE (folder) as I am."

WHY IS IT NECESSARY?
1. Portability: If we rename the folder from 'notes_app' to 'my_app' later, this code 
   still works because it doesn't hardcode the folder name.
2. Namespace Isolation: It prevents confusion if you have another file named 'database.py' 
   somewhere else in your project.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base

class Note(Base):
    """
    Represents the 'notes' table in our SQLite database.
    SQLAlchemy converts this Python class into a SQL command like:
    CREATE TABLE notes (id INTEGER PRIMARY KEY, title VARCHAR, ...);
    """
    __tablename__ = "notes"

    # WHY index=True? 
    # It makes searching by this column faster (e.g., finding a note by ID).
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    
    # Text is used for long content, String has a character limit (usually 255).
    content = Column(Text)
    
    # default=datetime.utcnow ensures the database auto-fills the time if we don't provide it.
    created_at = Column(DateTime, default=datetime.utcnow)