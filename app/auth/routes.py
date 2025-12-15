"""
app/auth/routes.py
------------------
Authentication blueprint for the Secure Notes App.

Purpose:
- Handles user registration, login, and logout.
- Provides basic authentication functionality.

v0.9.2: Functional baseline - INTENTIONALLY INSECURE
- Uses string concatenation for SQL queries (SQL injection vulnerable)
- Passwords stored in plaintext (no bcrypt)
- Basic Flask session management (no Flask-Login yet)
- No CSRF protection
- No rate limiting
- Security hardening will be added in v2.x
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.db import get_db

# Blueprint definition
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    User registration route - handles both GET (show form) and POST (create user).

    Returns:
        GET: Renders the registration form.
        POST: Creates user in DB and redirects to login.
    """
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        # Basic validation (minimal - no proper sanitisation)
        if not username or not password:
            flash("Username and password are required.", "error")
            return render_template(
                "auth/register.html",
                title="Register - Secure Notes"
            )

        db = get_db()

        # Check if username already exists
        # INSECURE: String concatenation - vulnerable to SQL injection
        check_query = f"SELECT * FROM users WHERE username = '{username}'"
        existing_user = db.execute(check_query).fetchone()

        if existing_user:
            flash("Username already exists. Please choose another.", "error")
            return render_template(
                "auth/register.html",
                title="Register - Secure Notes"
            )

        # Insert new user into database
        # INSECURE: String concatenation - vulnerable to SQL injection
        # INSECURE: Password stored in plaintext (no hashing)
        insert_query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
        db.execute(insert_query)
        db.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))

    # GET request - show registration form
    return render_template(
        "auth/register.html",
        title="Register - Secure Notes"
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    User login route - handles both GET (show form) and POST (authenticate user).

    Returns:
        GET: Renders the login form.
        POST: Authenticates user and creates session, redirects to notes dashboard.
    """
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        # Basic validation
        if not username or not password:
            flash("Username and password are required.", "error")
            return render_template(
                "auth/login.html",
                title="Login - Secure Notes"
            )

        db = get_db()

        # Authenticate user
        # INSECURE: String concatenation - vulnerable to SQL injection
        # INSECURE: Password comparison in plaintext (no hashing)
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        user = db.execute(query).fetchone()

        if user is None:
            flash("Invalid username or password.", "error")
            return render_template(
                "auth/login.html",
                title="Login - Secure Notes"
            )

        # Create session (basic - no Flask-Login yet)
        # INSECURE: No secure session configuration (no HttpOnly, Secure, SameSite flags)
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        flash(f"Welcome back, {user['username']}!", "success")
        return redirect(url_for("notes.notes_home"))

    # GET request - show login form
    return render_template(
        "auth/login.html",
        title="Login - Secure Notes"
    )


@auth_bp.route("/logout")
def logout():
    """
    User logout route - clears session and redirects to home.

    Returns:
        Redirects to home page after clearing session.
    """
    # Clear session
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))