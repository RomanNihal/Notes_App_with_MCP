"""
FILE: main.py
PURPOSE: The entry point of our API. It defines the URL routes.

WHY USE 'Depends'?
> db: Session = Depends(database.get_db)

This is 'Dependency Injection'.
Instead of manually opening a database connection inside every function 
(which is repetitive and error-prone), we tell FastAPI:
"I need a database session to run this function. Please go run 'get_db', 
give me the result, and clean it up when I'm done."
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
import os

# RELATIVE IMPORTS
# We import our other files using the dot notation.
# NOTE: This requires running the app as a module (python -m uvicorn notes_app.main:app)
from . import models, schemas, database

# Automatic Table Creation
# This looks at our models.py and creates the tables in SQLite if they don't exist.
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Professional Note Taking API")

@app.get("/")
def read_root():
    """Redirect root URL to the UI."""
    return RedirectResponse(url="/ui/")

# SERVING STATIC FILES (The Frontend)
# We calculate the absolute path to the 'static' folder to avoid path errors on Windows.
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/ui", StaticFiles(directory=static_path, html=True), name="static")

# --- API ENDPOINTS ---

@app.post("/notes/", response_model=schemas.NoteResponse)
def create_note(note: schemas.NoteCreate, db: Session = Depends(database.get_db)):
    """
    Create a new note.
    1. Validates input using 'NoteCreate' schema.
    2. Opens DB session.
    3. Saves data.
    4. Returns the saved object (including the new ID).
    """
    # Convert Pydantic schema -> SQLAlchemy model
    db_note = models.Note(title=note.title, content=note.content)
    
    db.add(db_note)      # Add to transaction
    db.commit()          # Save to file
    db.refresh(db_note)  # Reload to get the generated ID and created_at
    return db_note

@app.get("/notes/", response_model=List[schemas.NoteResponse])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    Get all notes with pagination.
    skip: How many to skip (for page 2, 3, etc.)
    limit: Max number to return (prevents crashing if you have 1M notes)
    """
    notes = db.query(models.Note).offset(skip).limit(limit).all()
    return notes

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(database.get_db)):
    """
    Delete a note by its ID.
    """
    # Try to find the note
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    
    # Handle the "Not Found" error gracefully
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()
    return {"status": "success", "message": "Note deleted"}