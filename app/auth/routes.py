"""
app/auth/routes.py
------------------
Authentication blueprint for the Secure Notes App.

Purpose:
- Handles user registration, login, and logout.
- Provides basic authentication functionality.

v0.9.2: Functional baseline - INTENTIONALLY INSECURE
- Uses string concatenation for SQL queries (SQL injection vulnerable)
- Password hashing with bcrypt (secure)
- Basic Flask session management (no Flask-Login yet)
- No CSRF protection
- No rate limiting
- Security hardening will be added in v2.x
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.db import get_db
import bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from app.auth.models import User
from app.auth.forms import RegistrationForm, LoginForm

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
    form = RegistrationForm()
    
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        
        db = get_db()
        
        # Insert new user into database
        # SECURE: Hash password with bcrypt before storing
        # Note: SQL injection still present (will be fixed with parameterized queries)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        insert_query = f"INSERT INTO users (username, password, role) VALUES ('{username}', '{password_hash}', 'user')"
        db.execute(insert_query)
        db.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))
    
    # GET request or validation failed - show form
    return render_template(
        "auth/register.html",
        title="Register - Secure Notes",
        form=form
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    User login route - handles both GET (show form) and POST (authenticate user).

    Returns:
        GET: Renders the login form.
        POST: Authenticates user and creates session, redirects to notes dashboard.
    """
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data

        db = get_db()

        # Authenticate user
        # SECURE: Get user by username only, then verify password hash
        # Note: SQL injection still present (will be fixed with parameterized queries)
        query = f"SELECT * FROM users WHERE username = '{username}'"
        user = db.execute(query).fetchone()

        if user:
            # Verify password using bcrypt
            stored_hash = user['password'].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                # Password correct - proceed with login
                pass  # User is valid, continue with session creation
            else:
                # Password incorrect
                user = None
        if user is None:
            flash("Invalid username or password.", "error")
            return render_template(
                "auth/login.html",
                title="Login - Secure Notes",
                form=form
            )

        # SECURE: Use Flask-Login for session management
        user_obj = User(user['id'], user['username'])
        login_user(user_obj, remember=False)

        flash(f"Welcome back, {user['username']}!", "success")
        return redirect(url_for("notes.notes_home"))
    
    # GET request - show login form
    return render_template(
        "auth/login.html",
        title="Login - Secure Notes",
        form=form
    )


@auth_bp.route("/logout")
def logout():
    """
    User logout route - clears session and redirects to home.

    Returns:
        Redirects to home page after clearing session.
    """
    # SECURE: Use Flask-Login logout
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))