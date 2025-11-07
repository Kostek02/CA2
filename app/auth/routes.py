"""
app/auth/routes.py
------------------
Authentication blueprint for the Secure Notes App.

Purpose:
- Handles user registration, login, and logout page rendering.
- Extends the base template for visual consistency.
- Prepares for form integration in v1.0-insecure-auth.
"""

from flask import Blueprint, render_template

# Blueprint definition
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    """
    Login page route.

    Returns:
        Renders the login.html template.
    """
    return render_template("auth/login.html", title="Login - Secure Notes")


@auth_bp.route("/register")
def register():
    """
    Registration page route.

    Returns:
        Renders the register.html template.
    """
    return render_template("auth/register.html", title="Register - Secure Notes")


@auth_bp.route("/logout")
def logout():
    """
    Logout route placeholder (will later redirect or flash).
    
    Returns:
        A plain text response for placeholder verification.
    """
    return "Auth Blueprint Active - Logout Route Placeholder"