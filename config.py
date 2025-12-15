""" 
config.py 
---------
Central configuration file for the Secure Notes Web Application.

Purpose:
- Load environment variables from .env file
- Provide a central point for application configuration
- Allow different configurations (Development, Production, etc.)

This design follows the Singleton pattern to ensure a 
    single instance of the configuration is used throughout the application and 
    follows the SOLID principles and follows Flask's best practice of separating 
    configuration from application logic.
"""

import os 

# Load environment variables from .env file
from dotenv import load_dotenv

# Load all variables from the .env file into the system environment
load_dotenv()

class Config:
    """ 
    The Config class defines key configuration options for the Flask app.

    Attributes:
        SECRET_KEY: The secret key for the application
        DEBUG: Enable/Disable debug mode
        FLASK_ENV: Controls the runtime environment (Development, Production, etc.)
    """

    # The secret key for the application
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key') 

    # Session cookie security settings (v2.0.2)
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
    SESSION_COOKIE_SECURE = False  # Set to True in production (requires HTTPS)
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes
    
    # Enable/Disable debug mode (convert to boolean)
    DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')
    
    # Controls the runtime environment (Development, Production, etc.)
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')

    # Rate Limiting (v2.3.1)
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'True').lower() == 'true'
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')