"""
app/notes/forms.py
------------------
WTForms classes for notes (v2.1.1).

Purpose:
- Define form structures with validation
- Provide CSRF protection via FlaskForm base class
- Sanitize and validate note input
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class NoteForm(FlaskForm):
    """
    Note creation/edit form with validation.
    
    Validators:
    - Title: Required, max 200 characters
    - Content: Required, max 10000 characters
    """
    title = StringField(
        'Title',
        validators=[
            DataRequired(message='Title is required.'),
            Length(max=200, message='Title must be less than 200 characters.')
        ],
        render_kw={'placeholder': 'Enter note title'}
    )
    
    content = TextAreaField(
        'Content',
        validators=[
            DataRequired(message='Content is required.'),
            Length(max=10000, message='Content must be less than 10000 characters.')
        ],
        render_kw={'rows': 10, 'placeholder': 'Enter note content'}
    )
    
    submit = SubmitField('Save Note')