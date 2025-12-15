"""
app/__init__.py
---------------
Main application factory for the Secure Notes App

Purpose:
- Implements the Flask "application factory" pattern.
- Loads configuration from config.py
- Registers blueprints (auth, notes, admin), database, helpers, error handlers, and middleware.
- Provides a home route to verify the app runs.
"""

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

# Import Blueprints
from app.auth.routes import auth_bp
from app.notes.routes import notes_bp
from app.admin.routes import admin_bp

# Import database helper
from app.db import init_app as init_db

# Import new v0.5 modules
from app.helpers import init_app as init_helpers
from app.error_handlers import register_errorhandlers
from app.middleware import register_middleware

# Import Flask-Login v2.0.2
from flask_login import LoginManager

# Import Flask-Talisman v2.3.1
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Import audit logging
from app.audit import setup_logging

def create_app():
    """
    Factory function for creating and configuring the Flask app.

    Why a factory:
    - It allows flexible setup (testing, production, etc.)
    - Prevents circular imports
    - Supports extension loading and blueprints cleanly

    Returns:
        A fully configured Flask app instance.
    """

    # Step 1: Create Flask instance
    app = Flask(__name__)

    # Step 1.5: Load configuration from config.py (Config class)
    app.config.from_object("config.Config")

    # Step 1.6: Initialise Flask-Talisman (v2.3.1)
    # Security headers: CSP, HSTS, X-Frame-Options, etc.
    talisman = Talisman(
        app,
        force_https=False,  # Set to True in production
        strict_transport_security=True,
        strict_transport_security_max_age=31536000,  # 1 year
        content_security_policy={
            'default-src': "'self'",
            'script-src': "'self' 'unsafe-inline'",  # Allow inline scripts for Flask debug toolbar (dev only)
            'style-src': "'self' 'unsafe-inline'",  # Allow inline styles (dev only - remove in production)
            'img-src': "'self' data:",
            'font-src': "'self'",
            'connect-src': "'self'",
            'frame-ancestors': "'none'",
            'base-uri': "'self'",
            'form-action': "'self'"
        },
        # Note: Nonces disabled for development (templates use inline styles)
        # In production, remove 'unsafe-inline' and use nonces properly
        frame_options='DENY',
        x_content_type_options=True,
        referrer_policy='strict-origin-when-cross-origin'
    )

    # Step 1.7: Initialise Flask-Limiter (v2.3.1)
    # Rate limiting to prevent brute force attacks
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,  # Rate limit by IP address
        default_limits=["200 per day", "50 per hour"],  # Global limits
        storage_uri="memory://"  # In-memory storage
    )
    # Store limiter on app for access in blueprints
    app.limiter = limiter

    # Step 2: Initialise CSRF Protection (v2.1.1)
    # Note: Must be after config is loaded (needs SECRET_KEY)
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Step 2.5: Initialise Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to login if not authenticated
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Step 2.6: Initialise Audit Logging (v2.3.2)
    # Audit logging for authentication and CRUD operations
    setup_logging(app)

    @login_manager.user_loader
    def load_user(user_id):
        """
        Flask-Login callback to load user from session.

        Args:
            user_id: User ID from session

        Returns:
            User instance or None
        """
        from app.auth.models import User
        return User.get(user_id)

    # Step 3: Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(notes_bp, url_prefix="/notes")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Step 4: Initialise the database
    init_db(app)

    # Step 5: Register helpers (context processors, globals)
    init_helpers(app)

    # Step 6: Register error handlers (403/404/500)
    register_errorhandlers(app)

    # Step 7: Register middleware (before/after request)
    try:
        register_middleware(app)
    except ImportError:
        pass # Skip if middleware not yet implemented

    # Step 8: Define home route
    @app.route("/")
    @app.route("/home")
    def home():
        """
        Render the home page.

        Returns:
            A rendered template of the home page.
        """
        return render_template("home.html", title="Home")

    # Step 8.5: Make limiter available for import
    app.limiter = limiter

    # Step 9: Return the configured Flask app
    return app