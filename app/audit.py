"""
app/audit.py
------------
Audit logging utility for the Secure Notes App.

Purpose:
- Centralized audit logging for authentication and CRUD operations
- Error logging for security events
- Log rotation to prevent disk space issues

v2.3.2: Audit Logging & Monitoring (SR8, SR9)
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from flask import request, has_request_context
from flask_login import current_user


def setup_logging(app):
    """
    Initialize logging configuration for the Flask app.
    
    Creates two log files:
    - logs/audit.log: Authentication and CRUD operations
    - logs/error.log: Errors and security events
    
    Args:
        app: Flask application instance
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(app.instance_path, '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure audit logger
    audit_logger = logging.getLogger('audit')
    audit_logger.setLevel(logging.INFO)
    audit_handler = RotatingFileHandler(
        os.path.join(log_dir, 'audit.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    audit_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    audit_handler.setFormatter(audit_formatter)
    audit_logger.addHandler(audit_handler)
    audit_logger.propagate = False
    
    # Configure error logger
    error_logger = logging.getLogger('error')
    error_logger.setLevel(logging.ERROR)
    error_handler = RotatingFileHandler(
        os.path.join(log_dir, 'error.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    error_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    error_handler.setFormatter(error_formatter)
    error_logger.addHandler(error_handler)
    error_logger.propagate = False


def get_user_identifier():
    """
    Get user identifier for logging (user ID or 'anonymous').
    
    Returns:
        str: User ID if authenticated, 'anonymous' otherwise
    """
    if has_request_context():
        try:
            if current_user.is_authenticated:
                return str(current_user.id)
        except:
            pass
    return 'anonymous'


def get_client_ip():
    """
    Get client IP address for logging.
    
    Returns:
        str: Client IP address or 'unknown'
    """
    if has_request_context():
        return request.remote_addr or 'unknown'
    return 'unknown'


def log_auth_event(action, result, username=None, details=None):
    """
    Log authentication events (login, logout, register).
    
    Args:
        action: Action type ('LOGIN', 'LOGOUT', 'REGISTER')
        result: Result ('SUCCESS', 'FAILURE')
        username: Username (optional, for login/register)
        details: Additional details (optional)
    """
    logger = logging.getLogger('audit')
    user_id = get_user_identifier()
    ip = get_client_ip()
    
    message = f"USER: {user_id} | ACTION: {action} | RESULT: {result}"
    if username:
        message += f" | USERNAME: {username}"
    message += f" | IP: {ip}"
    if details:
        message += f" | DETAILS: {details}"
    
    logger.info(message)


def log_crud_event(action, resource_type, resource_id, result, details=None):
    """
    Log CRUD operations (create, read, update, delete).
    
    Args:
        action: Action type ('CREATE', 'READ', 'UPDATE', 'DELETE')
        resource_type: Resource type ('NOTE', 'USER', etc.)
        resource_id: Resource ID
        result: Result ('SUCCESS', 'DENIED', 'NOT_FOUND')
        details: Additional details (optional)
    """
    logger = logging.getLogger('audit')
    user_id = get_user_identifier()
    ip = get_client_ip()
    
    message = f"USER: {user_id} | ACTION: {action}_{resource_type} | RESOURCE_ID: {resource_id} | RESULT: {result} | IP: {ip}"
    if details:
        message += f" | DETAILS: {details}"
    
    if result == 'DENIED':
        logger.warning(message)
    else:
        logger.info(message)


def log_error(error_type, message, details=None):
    """
    Log errors and security events.
    
    Args:
        error_type: Error type ('403', '404', '429', '500', etc.)
        message: Error message
        details: Additional details (optional)
    """
    logger = logging.getLogger('error')
    user_id = get_user_identifier()
    ip = get_client_ip()
    
    log_message = f"ERROR_TYPE: {error_type} | USER: {user_id} | IP: {ip} | MESSAGE: {message}"
    if details:
        log_message += f" | DETAILS: {details}"
    
    logger.error(log_message)