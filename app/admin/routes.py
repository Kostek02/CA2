"""
app/admin/routes.py
-------------------
Admin blueprint for the Secure Notes App.

Purpose:
- Handles administrative views for managing users and notes.
- Shows all users and notes in the system.

v0.9.3: Functional baseline - INTENTIONALLY INSECURE
- Uses string concatenation for SQL queries (SQL injection vulnerable)
- Shows plaintext passwords (demonstrates vulnerability)
- RBAC implemented in v2.2.1
"""

from flask import Blueprint, render_template, session
from app.db import get_db
from flask_login import login_required
from app.rbac import admin_required
from app.audit import log_crud_event

# Blueprint definition
admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@admin_required  # v2.2.1: Require admin role
@login_required
def admin_home():
    """
    Admin dashboard route - displays all users and notes.

    v2.2.1: Only admins can access

    Returns:
        Renders the admin dashboard with all users and notes or 403 error
    """
    db = get_db()

    # Fetch all users from database
    # INSECURE: String concatenation - vulnerable to SQL injection
    users_query = "SELECT * FROM users ORDER BY id"
    users = db.execute(users_query).fetchall()

    # Fetch all notes with user information (LEFT JOIN to get username)
    # INSECURE: String concatenation - vulnerable to SQL injection
    notes_query = """
        SELECT notes.*, users.username 
        FROM notes 
        LEFT JOIN users ON notes.user_id = users.id 
        ORDER BY notes.created_at DESC
    """
    notes = db.execute(notes_query).fetchall()

    # v2.3.2: Log admin dashboard access
    user_count = len(users)
    note_count = len(notes)
    log_crud_event('READ', 'ADMIN_DASHBOARD', 'all', 'SUCCESS', details=f'Users: {user_count}, Notes: {note_count}')

    return render_template(
        "admin/dashboard.html",
        title="Admin Dashboard - Secure Notes",
        users=users,
        notes=notes
    )