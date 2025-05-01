import pytest
from app import DrinkEntry, DailySummary, db
from datetime import datetime

def test_add_drink_page(logged_in_client):
    response = logged_in_client.get('/adddrink')
    assert response.status_code == 200
    assert b'Add a New Drink!' in response.data

def test_add_drink(logged_in_client):
    response = logged_in_client.post('/adddrink', data={
        'drink_name': 'Test Coffee',
        'caffeine_amount': '100',
        'mood': 'Energized'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    # Verify drink was added
    with logged_in_client.application.app_context():
        drink = DrinkEntry.query.first()
        assert drink is not None
        assert drink.drink_name == 'Test Coffee'
        assert drink.caffeine_amount == 100
        assert drink.mood == 'Energized'

def test_finish_day(logged_in_client):
    # First add some drinks
    with logged_in_client.application.app_context():
        drink1 = DrinkEntry(
            user_id=1,
            drink_name='Coffee 1',
            caffeine_amount=100,
            mood='Energized',
            date=datetime.now().date()
        )
        drink2 = DrinkEntry(
            user_id=1,
            drink_name='Coffee 2',
            caffeine_amount=150,
            mood='Alive',
            date=datetime.now().date()
        )
        db.session.add(drink1)
        db.session.add(drink2)
        db.session.commit()
    
    # Try to finish the day
    response = logged_in_client.post('/finish_day', follow_redirects=True)
    assert response.status_code == 200
    
    # Verify drinks were moved to daily summary
    with logged_in_client.application.app_context():
        summary = DailySummary.query.first()
        assert summary is not None
        assert summary.total_caffeine == 250
        assert summary.average_mood in ['Energized', 'Alive']
        
        # Verify drinks were deleted
        drinks = DrinkEntry.query.all()
        assert len(drinks) == 0

def test_finish_day_no_drinks(logged_in_client):
    response = logged_in_client.post('/finish_day', follow_redirects=True)
    assert response.status_code == 200
    assert b'No drinks to summarize for today' in response.data 