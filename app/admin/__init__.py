"""
app/admin/__init__.py
---------------------
Admin blueprint package initializer.

Purpose:
- Exposes the admin blueprint for import into the main app factory.
- Keeps administrative routes and logic isolated from other modules.
"""

from app.admin.routes import admin_bp