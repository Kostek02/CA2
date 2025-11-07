"""
app/admin/routes.py
-------------------
Admin blueprint for the Secure Notes App.

Purpose:
- Handles administrative views for managing users and notes.
- Demonstrates separation of privileged routes.
- Prepares for secure role-based access control (RBAC).
"""

from flask import Blueprint

# Blueprint definition
admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
def admin_home():
    """
    Admin dashboard route placeholder.

    Returns:
        A plain text response confirming the Admin blueprint is active.
    """
    return "Admin Blueprint Active - Admin Dashboard Placeholder"