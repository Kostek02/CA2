"""
tests/test_notes.py
-------------------
Tests for notes CRUD routes.

v1.5.1: Basic route validation - status codes
Note: No ownership checks yet (IDOR vulnerability present)
"""


def test_notes_home_get(client):
    """Test notes dashboard loads (GET request)."""
    response = client.get('/notes/')
    assert response.status_code == 200
    assert b'Notes' in response.data or b'notes' in response.data


def test_create_note_get(client):
    """Test create note page loads (GET request)."""
    response = client.get('/notes/create')
    assert response.status_code == 200
    assert b'Create' in response.data or b'create' in response.data


def test_create_note_post(client):
    """Test note creation (POST request)."""
    response = client.post('/notes/create', data={
        'title': 'Test Note Title',
        'content': 'Test note content for pytest'
    }, follow_redirects=True)
    assert response.status_code == 200
    # Should redirect to notes dashboard
    assert b'Notes' in response.data or b'notes' in response.data


def test_view_note(client):
    """Test viewing a note."""
    # First create a note
    client.post('/notes/create', data={
        'title': 'View Test Note',
        'content': 'Content to view in test'
    })
    
    # Then view it (assuming it gets ID 1)
    response = client.get('/notes/view/1')
    assert response.status_code == 200
    assert b'View Test Note' in response.data


def test_edit_note_get(client):
    """Test edit note page loads (GET request)."""
    # First create a note
    client.post('/notes/create', data={
        'title': 'Edit Test Note',
        'content': 'Original content'
    })
    
    # Then get edit page
    response = client.get('/notes/edit/1')
    assert response.status_code == 200
    assert b'Edit' in response.data or b'edit' in response.data


def test_edit_note_post(client):
    """Test note update (POST request)."""
    # First create a note
    client.post('/notes/create', data={
        'title': 'Original Title',
        'content': 'Original content'
    })
    
    # Then edit it
    response = client.post('/notes/edit/1', data={
        'title': 'Updated Title',
        'content': 'Updated content'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Updated Title' in response.data


def test_delete_note(client):
    """Test note deletion."""
    # First create a note
    client.post('/notes/create', data={
        'title': 'Note to Delete',
        'content': 'This will be deleted'
    })
    
    # Then delete it
    response = client.get('/notes/delete/1', follow_redirects=True)
    assert response.status_code == 200
    # Should redirect to notes dashboard
    assert b'Notes' in response.data or b'notes' in response.data