import os
import sys
import pytest
import tempfile
from datetime import datetime

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, User, DrinkEntry, DailySummary
from flask_login import login_user

@pytest.fixture
def client():
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def test_user():
    user = User(
        username='testuser',
        email='test@example.com',
        caffeine_goal=400
    )
    user.set_password('testpass')
    return user

@pytest.fixture
def logged_in_client(client, test_user):
    with app.app_context():
        db.session.add(test_user)
        db.session.commit()
        with client.session_transaction() as sess:
            sess['_user_id'] = str(test_user.id)
    return client 