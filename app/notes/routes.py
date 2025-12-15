"""
app/notes/routes.py
-------------------
Notes blueprint for the Secure Notes App.

Purpose:
- Manages CRUD operations for user notes.
- Provides isolated blueprint structure for modular development.

v0.9.1: Functional baseline - INTENTIONALLY INSECURE
- Uses string concatenation for SQL queries (SQL injection vulnerable)
- No input sanitisation
- No ownership checks
- No CSRF protection
- Security hardening will be added in v2.x
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.db import get_db
from flask_login import login_required, current_user

# Blueprint definition
notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/")
@login_required
def notes_home():
    '''
    Notes dashboard route - displays notes.
    
    v0.9.3: Shows all notes (no filtering yet - IDOR vulnerable)
    Will add user filtering in v2.2.1 with ownership checks.
    
    Returns:
        Renders the notes dashboard page with a list of notes.
    '''
    db = get_db()
    # INSECURE: No filtering by user_id - shows all notes (IDOR vulnerability)
    # No ownership checks - anyone can see/edit/delete any note
    notes = db.execute(
        "SELECT * FROM notes ORDER BY created_at DESC"
    ).fetchall()
    return render_template(
        "notes/dashboard.html",
        title="Notes Dashboard - Secure Notes",
        notes=notes
    )


@notes_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_note():
    """
    Note creation route - handles both GET (show form) and POST (create note).

    Returns:
        GET: Renders the note creation form.
        POST: Creates note in DB and redirects to dashboard.
    """
    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")

        # Basic validation (minimal - no proper sanitisation)
        if not title or not content:
            flash("Title and content are required.", "error")
            return render_template(
                "notes/create.html",
                title="Create Note - Secure Notes"
            )

        # Get user_id from session (if logged in)
        user_id = current_user.id if current_user.is_authenticated else None
        
        # Insert note into database
        # INSECURE: String concatenation - vulnerable to SQL injection
        # Links note to user via user_id (but no ownership validation yet)
        db = get_db()
        if user_id:
            insert_query = f"INSERT INTO notes (title, content, user_id) VALUES ('{title}', '{content}', {user_id})"
        else:
            # If not logged in, user_id is NULL (v0.9.1 behavior)
            insert_query = f"INSERT INTO notes (title, content, user_id) VALUES ('{title}', '{content}', NULL)"
        
        db.execute(insert_query)
        db.commit()

        flash("Note created successfully!", "success")
        return redirect(url_for("notes.notes_home"))

    # GET request - show form
    return render_template(
        "notes/create.html",
        title="Create Note - Secure Notes"
    )


@notes_bp.route("/view/<int:note_id>")
@login_required
def view_note(note_id):
    """
    Note viewing route - displays a single note in read-only mode.

    Args:
        note_id (int): ID of the note to view.

    Returns:
        Renders the note viewing page, or 404 if note not found.
    """
    db = get_db()
    # INSECURE: String concatenation - vulnerable to SQL injection
    # No ownership check - anyone can view any note
    query = f"SELECT * FROM notes WHERE id = {note_id}"
    note = db.execute(query).fetchone()

    if note is None:
        flash("Note not found.", "error")
        return redirect(url_for("notes.notes_home"))

    return render_template(
        "notes/view.html",
        title=f"View Note - Secure Notes",
        note=note
    )


@notes_bp.route("/edit/<int:note_id>", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    """
    Note editing route - handles both GET (show form) and POST (update note).

    Args:
        note_id (int): ID of the note to edit.

    Returns:
        GET: Renders the note editing form with pre-filled data.
        POST: Updates note in DB and redirects to dashboard.
    """
    db = get_db()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        # Basic validation (minimal - no proper sanitisation)
        if not title or not content:
            flash("Title and content are required.", "error")
            # Fetch note for re-rendering form
            query = f"SELECT * FROM notes WHERE id = {note_id}"
            note = db.execute(query).fetchone()
            return render_template(
                "notes/edit.html",
                title=f"Edit Note - Secure Notes",
                note=note
            )

        # Update note in database
        # INSECURE: String concatenation - vulnerable to SQL injection
        # No ownership check - anyone can edit any note (IDOR vulnerability)
        query = f"UPDATE notes SET title = '{title}', content = '{content}' WHERE id = {note_id}"
        db.execute(query)
        db.commit()

        flash("Note updated successfully!", "success")
        return redirect(url_for("notes.notes_home"))

    # GET request - fetch note and show form
    # INSECURE: String concatenation - vulnerable to SQL injection
    query = f"SELECT * FROM notes WHERE id = {note_id}"
    note = db.execute(query).fetchone()

    if note is None:
        flash("Note not found.", "error")
        return redirect(url_for("notes.notes_home"))

    return render_template(
        "notes/edit.html",
        title=f"Edit Note - Secure Notes",
        note=note
    )


@notes_bp.route("/delete/<int:note_id>")
@login_required
def delete_note(note_id):
    """
    Note deletion route - removes a note from the database.

    Args:
        note_id (int): ID of the note to delete.

    Returns:
        Redirects to dashboard after deletion.
    """
    db = get_db()

    # Check if note exists
    # INSECURE: String concatenation - vulnerable to SQL injection
    query = f"SELECT * FROM notes WHERE id = {note_id}"
    note = db.execute(query).fetchone()

    if note is None:
        flash("Note not found.", "error")
        return redirect(url_for("notes.notes_home"))

    # Delete note
    # INSECURE: String concatenation - vulnerable to SQL injection
    # No ownership check - anyone can delete any note (IDOR vulnerability)
    query = f"DELETE FROM notes WHERE id = {note_id}"
    db.execute(query)
    db.commit()

    flash("Note deleted successfully!", "success")
    return redirect(url_for("notes.notes_home"))