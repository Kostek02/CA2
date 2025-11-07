"""
app/notes/__init__.py
---------------------
Notes blueprint package initializer.

Purpose:
- Exposes the notes blueprint for import into the main app factory.
- Ensures modular separation of note-related routes and logic.
"""

from app.notes.routes import notes_bp