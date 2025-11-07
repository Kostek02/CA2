"""
app/auth/__init__.py
--------------------
Authentication blueprint package initializer.

Purpose:
- Exposes the authentication blueprint for import into the main app factory.
- Keeps the `auth` package modular and self-contained.
"""

from app.auth.routes import auth_bp