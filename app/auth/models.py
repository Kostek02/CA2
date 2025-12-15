"""
app/auth/models.py
------------------
User model for Flask-Login integration.

v2.0.2: Flask-Login User class with UserMixin
"""

from flask_login import UserMixin


class User(UserMixin):
    """
    User model for Flask-Login authentication.
    
    Implements UserMixin which provides:
    - is_authenticated
    - is_active
    - is_anonymous
    - get_id()
    """
    
    def __init__(self, user_id, username):
        """
        Initialize User instance.
        
        Args:
            user_id: Database user ID
            username: Username
        """
        self.id = user_id
        self.username = username
    
    @staticmethod
    def get(user_id):
        """
        Retrieve user from database by ID.
        
        Args:
            user_id: User ID to retrieve
            
        Returns:
            User instance or None if not found
        """
        from app.db import get_db
        
        db = get_db()
        # Note: SQL injection still present (will be fixed in v2.1.1)
        query = f"SELECT * FROM users WHERE id = {user_id}"
        user_row = db.execute(query).fetchone()
        
        if user_row:
            return User(user_row['id'], user_row['username'])
        return None