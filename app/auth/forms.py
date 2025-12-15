"""
app/auth/forms.py
-----------------
WTForms classes for authentication (v2.1.1).

Purpose:
- Define form structures with validation
- Provide CSRF protection via FlaskForm base class
- Sanitize and validate user input
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.db import get_db


class RegistrationForm(FlaskForm):
    """
    User registration form with validation.
    
    Validators:
    - Username: Required, 3-20 characters
    - Password: Required, minimum 6 characters
    - Custom: Check username uniqueness
    """
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required.'),
            Length(min=3, max=20, message='Username must be between 3 and 20 characters.')
        ],
        render_kw={'placeholder': 'Choose a username'}
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required.'),
            Length(min=6, message='Password must be at least 6 characters.')
        ],
        render_kw={'placeholder': 'Choose a password'}
    )
    
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """
        Custom validator: Check if username already exists.
        
        Args:
            username: Username field to validate
            
        Raises:
            ValidationError: If username already exists
        """
        db = get_db()
        # v2.3.3: Use parameterized query to prevent SQL injection
        query = "SELECT * FROM users WHERE username = ?"
        existing_user = db.execute(query, (username.data,)).fetchone()
        
        if existing_user:
            raise ValidationError('Username already exists. Please choose another.')


class LoginForm(FlaskForm):
    """
    User login form with validation.
    
    Validators:
    - Username: Required
    - Password: Required
    """
    username = StringField(
        'Username',
        validators=[DataRequired(message='Username is required.')],
        render_kw={'placeholder': 'Enter your username'}
    )
    
    password = PasswordField(
        'Password',
        validators=[DataRequired(message='Password is required.')],
        render_kw={'placeholder': 'Enter your password'}
    )
    
    submit = SubmitField('Login')