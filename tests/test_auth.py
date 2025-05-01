import pytest
from app import User, db

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'LOGIN' in response.data

def test_signup_page(client):
    response = client.get('/signup')
    assert response.status_code == 200
    assert b'SIGN UP' in response.data

def test_signup(client):
    response = client.post('/signup', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    # Verify user was created
    with client.application.app_context():
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'newuser@example.com'

def test_login(client, test_user):
    with client.application.app_context():
        db.session.add(test_user)
        db.session.commit()
    
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Today's Drinks" in response.data

def test_login_invalid_credentials(client, test_user):
    with client.application.app_context():
        db.session.add(test_user)
        db.session.commit()
    
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'wrongpass'
    })
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

def test_logout(logged_in_client):
    response = logged_in_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'LOGIN' in response.data  # Should be redirected to landing page 