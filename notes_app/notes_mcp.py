"""
FILE: notes_mcp.py
PURPOSE: The "Bridge" that allows AI models to control the Notes App.

INDUSTRY PATTERN:
We do NOT access the database directly here. 
Instead, we use HTTP requests to talk to the Backend API.
This ensures the AI follows the exact same security and validation rules as a human user.
"""

from mcp.server.fastmcp import FastMCP
import httpx

# 1. Initialize the MCP Server
# "dependencies" tells the MCP runtime what libraries this server needs (optional but good practice)
mcp = FastMCP("NotesApp", dependencies=["httpx"])

# The URL where your FastAPI backend is running
API_BASE_URL = "http://127.0.0.1:8000"

@mcp.tool()
async def create_new_note(title: str, content: str) -> str:
    """
    Create a new note. Use this when the user asks to save information, ideas, or reminders.
    
    Args:
        title: A short summary or headline for the note.
        content: The detailed body text of the note.
    """
    async with httpx.AsyncClient() as client:
        try:
            # The AI calls this tool -> We call the API
            response = await client.post(
                f"{API_BASE_URL}/notes/",
                json={"title": title, "content": content}
            )
            response.raise_for_status()
            data = response.json()
            return f"Success! Note created with ID {data['id']}."
        except httpx.HTTPError as e:
            return f"Error connecting to Notes App: {str(e)}"

@mcp.tool()
async def search_notes() -> str:
    """
    Read all existing notes. Use this when the user asks what is in their notebook 
    or wants to find specific information.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/notes/")
            response.raise_for_status()
            notes = response.json()
            
            if not notes:
                return "The notebook is currently empty."
            
            # Format the output so the AI can understand it easily
            result_text = "Here are the current notes:\n"
            for note in notes:
                result_text += f"- ID {note['id']} | Title: {note['title']} | Content: {note['content']}\n"
            return result_text
        except httpx.HTTPError as e:
            return f"Error reading notes: {str(e)}"

@mcp.tool()
async def delete_note_by_id(note_id: int) -> str:
    """
    Permanently delete a note.
    CRITICAL: You must ask the user for the specific Note ID before using this tool.
    Do not guess the ID.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f"{API_BASE_URL}/notes/{note_id}")
            if response.status_code == 404:
                return f"Error: Note with ID {note_id} was not found."
            response.raise_for_status()
            return f"Note {note_id} has been deleted."
        except httpx.HTTPError as e:
            return f"Error deleting note: {str(e)}"

if __name__ == "__main__":
    mcp.run()