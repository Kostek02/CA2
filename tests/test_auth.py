"""
tests/test_auth.py
------------------
Tests for authentication routes (register, login, logout).

v1.5.1: Basic route validation - status codes and redirects
"""


def test_register_get(client):
    """Test registration page loads (GET request)."""
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data


def test_register_post(client):
    """Test user registration (POST request)."""
    response = client.post('/auth/register', data={
        'username': 'testuser_pytest',
        'password': 'testpass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    # Should redirect to login page
    assert b'Login' in response.data or b'login' in response.data


def test_register_duplicate_username(client):
    """Test registration with duplicate username."""
    # Register first user
    client.post('/auth/register', data={
        'username': 'duplicate_user',
        'password': 'pass123'
    })
    
    # Try to register same username again
    response = client.post('/auth/register', data={
        'username': 'duplicate_user',
        'password': 'pass456'
    })
    assert response.status_code == 200
    assert b'already exists' in response.data or b'exists' in response.data


def test_login_get(client):
    """Test login page loads (GET request)."""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_login_post_invalid(client):
    """Test login with invalid credentials."""
    response = client.post('/auth/login', data={
        'username': 'nonexistent_user',
        'password': 'wrongpassword'
    })
    assert response.status_code == 200
    assert b'Invalid' in response.data or b'invalid' in response.data


def test_login_post_valid(client):
    """Test login with valid credentials."""
    # First register a user
    client.post('/auth/register', data={
        'username': 'valid_user',
        'password': 'validpass123'
    })
    
    # Then login
    response = client.post('/auth/login', data={
        'username': 'valid_user',
        'password': 'validpass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    # Should redirect to notes dashboard
    assert b'Notes' in response.data or b'notes' in response.data


def test_logout(client):
    """Test logout route redirects."""
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200