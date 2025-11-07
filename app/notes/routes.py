"""
app/notes/routes.py
-------------------
Notes blueprint for the Secure Notes App.

Purpose:
- Manages CRUD operations for user notes.
- Provides isolated blueprint structure for modular development.
- Prepares for secure data ownership and validation logic.
"""

from flask import Blueprint

# Blueprint definition
notes_bp = Blueprint("notes", __name__)

@notes_bp.route("/")
def notes_home():
    """
    Notes dashboard route.

    Returns:
        str: Plain text response confirming the Notes blueprint is active.
    """
    return "Notes Blueprint Active - Notes Dashboard Placeholder"


@notes_bp.route("/create")
def create_note():
    """
    Note creation route.

    Returns:
        str: Plain text response confirming the Notes blueprint is active.
    """
    return "Notes Blueprint Active - Create Note Placeholder"


@notes_bp.route("/view/<int:note_id>")
def view_note(note_id):
    """
    Note viewing route.

    Args:
        note_id (int): ID of the note to view.

    Returns:
        str: Plain text response including the note ID.
    """
    return f"Notes Blueprint Active - View Note {note_id} Placeholder"


@notes_bp.route("/edit/<int:note_id>")
def edit_note(note_id):
    """
    Note editing route.

    Args:
        note_id (int): ID of the note to edit.

    Returns:
        str: Plain text response including the note ID.
    """
    return f"Notes Blueprint Active - Edit Note {note_id} Placeholder"


@notes_bp.route("/delete/<int:note_id>")
def delete_note(note_id):
    """
    Note deletion route.

    Args:
        note_id (int): ID of the note to delete.

    Returns:
        str: Plain text response including the note ID.
    """
    return f"Notes Blueprint Active - Delete Note {note_id} Placeholder"
