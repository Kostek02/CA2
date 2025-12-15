"""
tests/test_admin.py
-------------------
Tests for admin routes.

v1.5.1: Basic route validation
Note: No access control yet (broken access control vulnerability present)
"""


def test_admin_home_get(client):
    """Test admin dashboard loads (GET request)."""
    response = client.get('/admin/')
    assert response.status_code == 200
    assert b'Admin' in response.data or b'admin' in response.data


def test_admin_shows_users(client):
    """Test admin dashboard displays users."""
    # Create a user first
    client.post('/auth/register', data={
        'username': 'admin_test_user',
        'password': 'adminpass123'
    })
    
    # Check admin dashboard
    response = client.get('/admin/')
    assert response.status_code == 200
    # Should show users table
    assert b'Users' in response.data or b'users' in response.data


def test_admin_shows_notes(client):
    """Test admin dashboard displays notes."""
    # Create a note first
    client.post('/notes/create', data={
        'title': 'Admin Test Note',
        'content': 'Note for admin dashboard test'
    })
    
    # Check admin dashboard
    response = client.get('/admin/')
    assert response.status_code == 200
    # Should show notes table
    assert b'Notes' in response.data or b'notes' in response.data