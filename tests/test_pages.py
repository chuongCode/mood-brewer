import pytest
from app import app, db, User, DrinkEntry, DailySummary
from datetime import datetime

def test_landing_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Mood Brewer' in response.data

def test_home_page_unauthorized(client):
    response = client.get('/home')
    assert response.status_code == 302  # Should redirect to login
    assert '/login' in response.location

def test_home_page_authorized(logged_in_client):
    response = logged_in_client.get('/home')
    assert response.status_code == 200
    assert b"Today's Drinks:" in response.data

def test_home_page_with_drinks(logged_in_client):
    # Add some drinks first
    with logged_in_client.application.app_context():
        drink1 = DrinkEntry(
            user_id=1,
            drink_name='Coffee 1',
            caffeine_amount=100,
            mood='energized',
            date=datetime.now().date()
        )
        db.session.add(drink1)
        db.session.commit()
    
    response = logged_in_client.get('/home')
    assert response.status_code == 200
    assert b'Coffee 1' in response.data
    assert b'100' in response.data
    assert b'energized' in response.data

def test_home_page_with_daily_summary(logged_in_client):
    # Add a daily summary
    with logged_in_client.application.app_context():
        summary = DailySummary(
            user_id=1,
            date=datetime.now().date(),
            total_caffeine=300,
            average_mood='energized'
        )
        db.session.add(summary)
        db.session.commit()
    
    response = logged_in_client.get('/caff_stat')
    assert response.status_code == 200
    assert b'300' in response.data
    assert b'energized' in response.data 