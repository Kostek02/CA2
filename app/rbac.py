"""
app/rbac.py
-----------
Role-Based Access Control (RBAC) helpers and decorators (v2.2.1).

Purpose:
- Provide decorators for role-based route protection
- Helper functions for ownership and permission checks
"""

from functools import wraps
from flask import abort
from flask_login import login_required, current_user
from app.db import get_db


def admin_required(f):
    """
    Decorator to require admin role.
    
    Usage:
        @admin_required
        @login_required
        def admin_route():
            ...
    """
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function


def moderator_required(f):
    """
    Decorator to require moderator or admin role.
    
    Usage:
        @moderator_required
        @login_required
        def moderator_route():
            ...
    """
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_moderator():
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function


def check_note_ownership(note_id, allow_admin=True):
    """
    Check if current user owns the note (or is admin if allow_admin=True).
    
    Args:
        note_id: Note ID to check
        allow_admin: If True, admins can access any note
        
    Returns:
        True if user owns note or is admin, False otherwise
        
    Raises:
        404: If note doesn't exist
        403: If user doesn't have permission
    """
    db = get_db()
    # Note: SQL injection still present (will be fixed with parameterized queries)
    query = f"SELECT * FROM notes WHERE id = {note_id}"
    note = db.execute(query).fetchone()
    
    if not note:
        abort(404)  # Note not found
    
    # Admin can access any note
    if allow_admin and current_user.is_admin():
        return True
    
    # Check ownership
    if note['user_id'] == current_user.id:
        return True
    
    # User doesn't own note and isn't admin
    abort(403)  # Forbidden


def can_edit_note(note_id):
    """
    Check if current user can edit the note.
    
    Rules:
    - User: Can edit own notes only
    - Moderator: Can edit own notes only (not others')
    - Admin: Can edit any note
    
    Args:
        note_id: Note ID to check
        
    Returns:
        True if user can edit, False otherwise
    """
    if current_user.is_admin():
        # Admin can edit any note (but check it exists)
        db = get_db()
        query = f"SELECT * FROM notes WHERE id = {note_id}"
        note = db.execute(query).fetchone()
        return note is not None
    
    # Regular users and moderators can only edit their own notes
    try:
        check_note_ownership(note_id, allow_admin=False)
        return True
    except:
        return False


def can_delete_note(note_id):
    """
    Check if current user can delete the note.
    
    Rules:
    - User: Can delete own notes only
    - Moderator: Can delete any note (moderation power)
    - Admin: Can delete any note
    
    Args:
        note_id: Note ID to check
        
    Returns:
        True if user can delete, False otherwise
    """
    if current_user.is_admin() or current_user.is_moderator():
        # Admin and Moderator can delete any note (but check it exists)
        db = get_db()
        query = f"SELECT * FROM notes WHERE id = {note_id}"
        note = db.execute(query).fetchone()
        return note is not None
    
    # Regular users can only delete their own notes
    try:
        check_note_ownership(note_id, allow_admin=False)
        return True
    except:
        return False


def can_view_note(note_id):
    """
    Check if current user can view the note.
    
    Rules:
    - User: Can view own notes only
    - Moderator: Can view all notes (read-only)
    - Admin: Can view all notes
    
    Args:
        note_id: Note ID to check
        
    Returns:
        True if user can view, False otherwise
    """
    if current_user.is_moderator() or current_user.is_admin():
        # Moderators and admins can view all notes
        db = get_db()
        query = f"SELECT * FROM notes WHERE id = {note_id}"
        note = db.execute(query).fetchone()
        return note is not None
    
    # Regular users can only view their own notes
    try:
        check_note_ownership(note_id, allow_admin=False)
        return True
    except:
        return False