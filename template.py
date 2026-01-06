import os
from pathlib import Path

# --- Configuration ---
PROJECT_NAME = "notes_app"
BASE_DIR = Path.cwd() / PROJECT_NAME

# --- Execution ---
def create_project_structure():
    # 1. Create main directory
    if not BASE_DIR.exists():
        BASE_DIR.mkdir()
        print(f"📂 Created directory: {BASE_DIR}")
    
    # 2. Create static directory for frontend
    static_dir = BASE_DIR / "static"
    static_dir.mkdir(exist_ok=True)
    print(f"📂 Created directory: {static_dir}")

    # 3. Create empty files
    files_to_create = [
        BASE_DIR / "database.py",
        BASE_DIR / "models.py",
        BASE_DIR / "schemas.py",
        BASE_DIR / "main.py",
        BASE_DIR / "__init__.py",
        static_dir / "index.html",
    ]

    for file_path in files_to_create:
        # 'touch' the file (create if not exists)
        with open(file_path, "w") as f:
            pass 
        print(f"📄 Created empty file: {file_path}")

    print(f"\n🚀 Success! Project structure ready in '{PROJECT_NAME}'")

if __name__ == "__main__":
    create_project_structure()