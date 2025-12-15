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
from app.audit import log_auth_event, log_error
# Blueprint definition
auth_bp = Blueprint("auth", __name__)


# v2.3.1: Rate limiting before_request hook
@auth_bp.before_request
def check_rate_limits():
    """v2.3.1: Apply rate limiting to auth routes."""
    if request.method == 'POST':
        from flask import current_app, abort
        from flask_limiter.errors import RateLimitExceeded
        from flask_limiter.util import get_remote_address
        limiter = getattr(current_app, 'limiter', None)
        if limiter:
            try:
                # Determine limit based on endpoint
                if request.endpoint == 'auth.register':
                    limit_str = "3 per minute"
                elif request.endpoint == 'auth.login':
                    limit_str = "5 per minute"
                else:
                    return  # No rate limit for other endpoints
                
                # Apply rate limit decorator to a dummy function
                def _check():
                    pass
                wrapped = limiter.limit(limit_str)(_check)
                wrapped()
            except RateLimitExceeded:
                # v2.3.2: Log rate limit trigger (before abort)
                log_error('RATE_LIMIT', f'Rate limit triggered for {request.endpoint}', details=f'IP: {get_remote_address()}, Limit: {limit_str}')
                abort(429)
            except Exception:
                # If limiter not properly configured, allow request
                pass


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    User registration route - handles both GET (show form) and POST (create user).
    
    v2.3.1: Rate limited to 3 attempts per minute.

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
        # Convert bytes to string for database storage
        password_hash_str = password_hash.decode('utf-8')
        insert_query = f"INSERT INTO users (username, password, role) VALUES ('{username}', '{password_hash_str}', 'user')"
        db.execute(insert_query)
        db.commit()

        # v2.3.2: Log registration event
        log_auth_event('REGISTER', 'SUCCESS', username=username)

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
    
    v2.3.1: Rate limited to 5 attempts per minute.

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
            stored_hash_str = user['password']
            # Convert string back to bytes for bcrypt
            try:
                stored_hash = stored_hash_str.encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                    # Password correct - proceed with login
                    pass  # User is valid, continue with session creation
                else:
                    # Password incorrect
                    user = None
            except (ValueError, AttributeError):
                # Invalid hash format (might be old plaintext password or corrupted)
                user = None
        if user is None:
            # v2.3.2: Log failed login attempt
            log_auth_event('LOGIN', 'FAILURE', username=username, details='Invalid credentials')
            log_error('AUTH_FAILURE', f'Failed login attempt for user: {username}')
            flash("Invalid username or password.", "error")
            return render_template(
                "auth/login.html",
                title="Login - Secure Notes",
                form=form
            )

        # SECURE: Use Flask-Login for session management
        user_obj = User(user['id'], user['username'])
        login_user(user_obj, remember=False)

        # v2.3.2: Log successful login
        log_auth_event('LOGIN', 'SUCCESS', username=username)

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
    # v2.3.2: Log logout event
    if current_user.is_authenticated:
        log_auth_event('LOGOUT', 'SUCCESS', username=current_user.username)
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))