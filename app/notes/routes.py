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

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from app.db import get_db
from flask_login import login_required, current_user
from app.notes.forms import NoteForm
from app.rbac import check_note_ownership, can_edit_note, can_delete_note, can_view_note
from app.audit import log_crud_event, log_error

# Blueprint definition
notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/")
@login_required
def notes_home():
    '''
    Notes dashboard route - displays notes filtered by role.
    
    v2.2.1: RBAC filtering
    - User: Shows only their own notes
    - Moderator/Admin: Shows all notes
    
    Returns:
        Renders the notes dashboard page with filtered list of notes.
    '''
    db = get_db()
    
    # v2.2.1: Filter notes by role
    if current_user.is_admin() or current_user.is_moderator():
        # Admin and Moderator can see all notes
        notes = db.execute(
            "SELECT * FROM notes ORDER BY created_at DESC"
        ).fetchall()
    else:
        # Regular users can only see their own notes
        # v2.3.3: Use parameterized query to prevent SQL injection
        query = "SELECT * FROM notes WHERE user_id = ? ORDER BY created_at DESC"
        notes = db.execute(query, (current_user.id,)).fetchall()
    
    # v2.3.2: Log dashboard access
    note_count = len(notes)
    role = 'admin' if current_user.is_admin() else 'moderator' if current_user.is_moderator() else 'user'
    log_crud_event('READ', 'DASHBOARD', 'all', 'SUCCESS', details=f'Role: {role}, Notes shown: {note_count}')
    
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
    form = NoteForm()
    
    if form.validate_on_submit():
        title = form.title.data.strip()
        content = form.content.data.strip()
        user_id = current_user.id
        
        # Insert note into database
        # v2.3.3: Use parameterized query to prevent SQL injection
        db = get_db()
        insert_query = "INSERT INTO notes (title, content, user_id) VALUES (?, ?, ?)"
        db.execute(insert_query, (title, content, user_id))
        db.commit()

        # v2.3.2: Log note creation
        note_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        log_crud_event('CREATE', 'NOTE', note_id, 'SUCCESS', details=f'Title: {title[:50]}')

        flash("Note created successfully!", "success")
        return redirect(url_for("notes.notes_home"))
    
    # GET request or validation failed - show form
    return render_template(
        "notes/create.html",
        title="Create Note - Secure Notes",
        form=form
    )

@notes_bp.route("/view/<int:note_id>")
@login_required
def view_note(note_id):
    """
    View a specific note.
    
    v2.2.1: RBAC check - user must own note OR be moderator/admin
    
    Args:
        note_id: ID of note to view
        
    Returns:
        Renders note view page or 403/404 error
    """
    # v2.2.1: Check if user can view this note
    if not can_view_note(note_id):
        # v2.3.2: Log denied view attempt
        db = get_db()
        # v2.3.3: Use parameterized query to prevent SQL injection
        query = "SELECT * FROM notes WHERE id = ?"
        note = db.execute(query, (note_id,)).fetchone()
        if note:
            log_crud_event('READ', 'NOTE', note_id, 'DENIED', details='Not owner')
            log_error('403', f'View denied for note {note_id}', details=f'User {current_user.id} attempted to view note owned by {note["user_id"]}')
        abort(403)  # Forbidden
    
    db = get_db()
    # v2.3.3: Use parameterized query to prevent SQL injection
    query = "SELECT * FROM notes WHERE id = ?"
    note = db.execute(query, (note_id,)).fetchone()
    
    if not note:
        abort(404)  # Not found
    
    # v2.3.2: Log note view
    log_crud_event('READ', 'NOTE', note_id, 'SUCCESS')
    
    return render_template(
        "notes/view.html",
        title=f"{note['title']} - Secure Notes",
        note=note
    )

@notes_bp.route("/edit/<int:note_id>", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    """
    Edit note route - handles both GET (show form) and POST (update note).
    
    v2.2.1: RBAC check - user must own note OR be admin
    - User: Can edit own notes only
    - Moderator: Can edit own notes only (not others')
    - Admin: Can edit any note
    
    Args:
        note_id: ID of note to edit
        
    Returns:
        GET: Renders edit form or 403/404 error
        POST: Updates note and redirects or 403/404 error
    """
    # v2.2.1: Check if user can edit this note
    if not can_edit_note(note_id):
        # v2.3.2: Log denied edit attempt
        db = get_db()
        # v2.3.3: Use parameterized query to prevent SQL injection
        query = "SELECT * FROM notes WHERE id = ?"
        note = db.execute(query, (note_id,)).fetchone()
        if note:
            log_crud_event('UPDATE', 'NOTE', note_id, 'DENIED', details='Not owner')
            log_error('403', f'Edit denied for note {note_id}', details=f'User {current_user.id} attempted to edit note owned by {note["user_id"]}')
        abort(403)  # Forbidden
    
    db = get_db()
    # v2.3.3: Use parameterized query to prevent SQL injection
    query = "SELECT * FROM notes WHERE id = ?"
    note = db.execute(query, (note_id,)).fetchone()
    
    if not note:
        abort(404)  # Not found
    
    form = NoteForm()
    
    if form.validate_on_submit():
        title = form.title.data.strip()
        content = form.content.data.strip()
        
        # v2.2.1: Double-check ownership/admin before updating
        if not can_edit_note(note_id):
            abort(403)
        
        # Update note in database
        # v2.3.3: Use parameterized query to prevent SQL injection
        update_query = "UPDATE notes SET title = ?, content = ? WHERE id = ?"
        db.execute(update_query, (title, content, note_id))
        db.commit()
        
        # v2.3.2: Log note edit
        log_crud_event('UPDATE', 'NOTE', note_id, 'SUCCESS', details=f'Title: {title[:50]}')
        
        flash("Note updated successfully!", "success")
        return redirect(url_for("notes.notes_home"))
    
    # GET request or validation failed - show form
    form.title.data = note['title']
    form.content.data = note['content']
    
    return render_template(
        "notes/edit.html",
        title=f"Edit Note - Secure Notes",
        form=form,
        note=note
    )

@notes_bp.route("/delete/<int:note_id>")
@login_required
def delete_note(note_id):
    """
    Delete note route.
    
    v2.2.1: RBAC check - user must own note OR be admin/moderator
    - User: Can delete own notes only
    - Moderator: Can delete any note (moderation power)
    - Admin: Can delete any note
    
    Args:
        note_id: ID of note to delete
        
    Returns:
        Redirects to dashboard or 403/404 error
    """
    # v2.2.1: Check if user can delete this note
    if not can_delete_note(note_id):
        # v2.3.2: Log denied delete attempt
        db = get_db()
        # v2.3.3: Use parameterized query to prevent SQL injection
        query = "SELECT * FROM notes WHERE id = ?"
        note = db.execute(query, (note_id,)).fetchone()
        if note:
            log_crud_event('DELETE', 'NOTE', note_id, 'DENIED', details='Not owner')
            log_error('403', f'Delete denied for note {note_id}', details=f'User {current_user.id} attempted to delete note owned by {note["user_id"]}')
        abort(403)  # Forbidden
    
    db = get_db()
    # v2.3.3: Use parameterized query to prevent SQL injection
    query = "SELECT * FROM notes WHERE id = ?"
    note = db.execute(query, (note_id,)).fetchone()
    
    if not note:
        abort(404)  # Not found
    
    # v2.2.1: Double-check ownership/admin before deleting
    if not can_delete_note(note_id):
        abort(403)
    
    # Delete note from database
    # v2.3.3: Use parameterized query to prevent SQL injection
    delete_query = "DELETE FROM notes WHERE id = ?"
    db.execute(delete_query, (note_id,))
    db.commit()
    
    # v2.3.2: Log note deletion
    log_crud_event('DELETE', 'NOTE', note_id, 'SUCCESS')
    
    flash("Note deleted successfully!", "success")
    return redirect(url_for("notes.notes_home"))