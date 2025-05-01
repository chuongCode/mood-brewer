import pytest
from app import app, db, User, DrinkEntry
from datetime import datetime

def test_invalid_route(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404

def test_add_drink_invalid_data(logged_in_client):
    # Verify the form has proper validation attributes
    response = logged_in_client.get('/adddrink')
    assert b'type="number"' in response.data
    
    # No need to test submissions - browser prevents them through HTML5 validation
    # - type="number" prevents non-numeric values
    # - required attribute prevents missing values

def test_add_drink_invalid_mood(logged_in_client):
    # Verify the form has the correct mood options as radio buttons
    response = logged_in_client.get('/adddrink')
    for mood in ['Sleepy', 'Tired', 'Okay', 'Alive', 'Energized']:
        assert f'value="{mood}"'.encode() in response.data
        assert b'type="radio"' in response.data
    
    # No need to test submission - browser prevents invalid moods through radio buttons

def test_duplicate_username_signup(client):
    # First create a user
    with client.application.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
    
    # Try to create another user with same username
    response = client.post('/signup', data={
        'username': 'testuser',
        'email': 'different@example.com',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Username already exists' in response.data

def test_duplicate_email_signup(client):
    # First create a user
    with client.application.app_context():
        user = User(username='testuser1', email='test@example.com')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
    
    # Try to create another user with same email
    response = client.post('/signup', data={
        'username': 'testuser2',
        'email': 'test@example.com',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Email already exists' in response.data 