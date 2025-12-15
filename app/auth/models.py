"""
app/auth/models.py
------------------
User model for Flask-Login integration with RBAC (v2.2.1).
"""

from flask_login import UserMixin


class User(UserMixin):
    """
    User model for Flask-Login authentication with role support.
    
    Implements UserMixin which provides:
    - is_authenticated
    - is_active
    - is_anonymous
    - get_id()
    
    v2.2.1: Added role attribute for RBAC
    """
    
    def __init__(self, user_id, username, role='user'):
        """
        Initialize User instance.
        
        Args:
            user_id: Database user ID
            username: Username
            role: User role ('user', 'moderator', 'admin')
        """
        self.id = user_id
        self.username = username
        self.role = role  # v2.2.1: Added role
    
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
        # Note: SQL injection still present (will be fixed with parameterized queries)
        query = f"SELECT * FROM users WHERE id = {user_id}"
        user_row = db.execute(query).fetchone()
        
        if user_row:
            # v2.2.1: Load role from database
            try:
                role = user_row['role'] or 'user'  # Handle NULL values
            except (KeyError, IndexError):
                role = 'user'  # Default to 'user' if role column doesn't exist
            return User(user_row['id'], user_row['username'], role)
        return None
    
    def is_admin(self):
        """Check if user is an admin."""
        return self.role == 'admin'
    
    def is_moderator(self):
        """Check if user is a moderator or admin."""
        return self.role in ('moderator', 'admin')
    
    def is_user(self):
        """Check if user is a regular user."""
        return self.role == 'user'