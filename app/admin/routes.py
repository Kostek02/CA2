"""
app/admin/routes.py
-------------------
Admin blueprint for the Secure Notes App.

Purpose:
- Handles administrative views for managing users and notes.
- Shows all users and notes in the system.

v0.9.3: Functional baseline - INTENTIONALLY INSECURE
- Uses string concatenation for SQL queries (SQL injection vulnerable)
- No access control - anyone can access admin route (will be fixed in v2.2.1)
- Shows plaintext passwords (demonstrates vulnerability)
- No RBAC - no role-based restrictions
"""

from flask import Blueprint, render_template, session
from app.db import get_db
from flask_login import login_required

# Blueprint definition
admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@login_required
def admin_home():
    """
    Admin dashboard route - displays all users and notes.

    v0.9.3: No access control - anyone can access (vulnerability)
    Will add RBAC in v2.2.1 to restrict to admin users only.

    Returns:
        Renders the admin dashboard with all users and notes.
    """
    db = get_db()

    # Fetch all users from database
    # INSECURE: String concatenation - vulnerable to SQL injection
    # INSECURE: No access control - anyone can view all users
    users_query = "SELECT * FROM users ORDER BY id"
    users = db.execute(users_query).fetchall()

    # Fetch all notes with user information (LEFT JOIN to get username)
    # INSECURE: String concatenation - vulnerable to SQL injection
    # Shows all notes regardless of ownership (IDOR vulnerability)
    notes_query = """
        SELECT notes.*, users.username 
        FROM notes 
        LEFT JOIN users ON notes.user_id = users.id 
        ORDER BY notes.created_at DESC
    """
    notes = db.execute(notes_query).fetchall()

    return render_template(
        "admin/dashboard.html",
        title="Admin Dashboard - Secure Notes",
        users=users,
        notes=notes
    )