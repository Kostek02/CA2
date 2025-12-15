"""
app/error_handlers.py
---------------------
Centralised custom error handling for the Secure Notes App.

Purpose:
- Register consistent templates for HTTP errors (403, 404, 500)
- Prevents stack traces from appearing in production
- Demonstrates secure error management principles (SR9)
"""

from flask import render_template, flash

def register_errorhandlers(app):
    """
    Register custom error handlers for common HTTP errors.
    """

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template("403.html", title="Forbidden"), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("404.html", title="Not Found"), 404

    @app.errorhandler(500)
    def internal_error(error):
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
        flash("Too many requests. Please try again later.", "error")
        return render_template("429.html", title="Rate Limit Exceeded"), 429
