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

    # Step 2: Load configuratoin from config.py (Config class)
    app.config.from_object("config.Config")

    # Step 2.5: Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to login if not authenticated
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

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

    # Step 9: Return the configured Flask app
    return app