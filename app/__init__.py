"""
app/__init__.py
---------------
Main application factory for the Secure Notes App

Purpose:
- Implements the Flask "application factory" pattern.
- Loads configuration from config.py
- Defines simple base route to verify the app runs.
- Prepares for future blueprint registration (auth, notes, admin).
"""

from flask import Flask, render_template

# Import Blueprints
from app.auth.routes import auth_bp
from app.notes.routes import notes_bp
from app.admin.routes import admin_bp

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

    # Step 3: Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(notes_bp, url_prefix="/notes")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Step 4: Create a home route
    @app.route("/")
    @app.route("/home")
    def home():
        """
        Render the home page.

        Returns:
            A rendered template of the home page.
        """
        return render_template("home.html", title="Home")

    # Step 5: Return the configured Flask app
    return app