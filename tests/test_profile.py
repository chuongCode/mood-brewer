import pytest
from app import User, db

def test_profile_page(logged_in_client):
    response = logged_in_client.get('/profile')
    assert response.status_code == 200
    assert b'Username:' in response.data

def test_update_caffeine_goal(logged_in_client):
    response = logged_in_client.post('/update_goal', data={
        'caffeine_goal': '500'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    # Verify goal was updated
    with logged_in_client.application.app_context():
        user = User.query.first()
        assert user.caffeine_goal == 500

def test_update_caffeine_goal_invalid(logged_in_client):
    response = logged_in_client.post('/update_goal', data={
        'caffeine_goal': 'invalid'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid input for caffeine goal' in response.data
    
    # Verify goal was not updated
    with logged_in_client.application.app_context():
        user = User.query.first()
        assert user.caffeine_goal == 400  # Default value 