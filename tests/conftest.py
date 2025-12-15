"""
tests/conftest.py
-----------------
Pytest configuration and fixtures for Flask app testing.

v1.5.1: Basic fixtures for route testing (insecure baseline)
"""

import pytest
import os
import tempfile
from app import create_app
from app.db import get_db, init_db


@pytest.fixture
def app():
    """
    Create application for testing with temporary database.
    
    Returns:
        Flask app instance configured for testing.
    """
    import shutil
    from pathlib import Path
    
    # Create temporary directory for instance folder (where DB will be stored)
    instance_path = tempfile.mkdtemp()
    
    # Create app (no parameters - create_app() doesn't accept config)
    app = create_app()
    
    # Configure for testing
    app.config['TESTING'] = True
    app.instance_path = instance_path
    
    # Copy schema.sql to temporary instance path
    schema_source = Path(__file__).parent.parent / 'instance' / 'schema.sql'
    schema_dest = Path(instance_path) / 'schema.sql'
    if schema_source.exists():
        shutil.copy(schema_source, schema_dest)
    
    # Initialize database schema
    with app.app_context():
        init_db()
    
    yield app
    
    # Cleanup: remove temporary instance directory
    if os.path.exists(instance_path):
        shutil.rmtree(instance_path)


@pytest.fixture
def client(app):
    """
    Create test client for making requests.
    
    Args:
        app: Flask app instance from app fixture.
    
    Returns:
        Flask test client.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Create CLI test runner for Flask app.
    
    Args:
        app: Flask app instance from app fixture.
    
    Returns:
        Flask CLI test runner.
    """
    return app.test_cli_runner()