"""
app/error_handlers.py
---------------------
Centralised custom error handling for the Secure Notes App.

Purpose:
- Register consistent templates for HTTP errors (403, 404, 500)
- Prevents stack traces from appearing in production
- Demonstrates secure error management principles (SR9)
"""

from flask import render_template, flash, request
from app.audit import log_error

def register_errorhandlers(app):
    """
    Register custom error handlers for common HTTP errors.
    """

    @app.errorhandler(403)
    def forbidden_error(error):
        # v2.3.2: Log 403 error
        log_error('403', 'Access denied', details=f'Path: {request.path}')
        return render_template("403.html", title="Forbidden"), 403

    @app.errorhandler(404)
    def not_found_error(error):
        # v2.3.2: Log 404 error
        log_error('404', 'Resource not found', details=f'Path: {request.path}')
        return render_template("404.html", title="Not Found"), 404

    @app.errorhandler(500)
    def internal_error(error):
        # v2.3.2: Log 500 error
        log_error('500', 'Internal server error', details=f'Path: {request.path}')
        return render_template("500.html", title="Server Error"), 500

    @app.errorhandler(429)
    def ratelimit_handler(e):
        '''
        Custom handler for rate limit errors (v2.3.1).
        
        Args:
            e: The 429 error exception
            
        Returns:
            Rendered 429 error page with 429 status code
        '''
        # v2.3.2: Log 429 error
        log_error('429', 'Rate limit exceeded', details=f'Endpoint: {request.endpoint}, IP: {request.remote_addr}')
        flash("Too many requests. Please try again later.", "error")
        return render_template("429.html", title="Rate Limit Exceeded"), 429
