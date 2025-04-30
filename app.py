from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
from dotenv import load_dotenv
from datetime import datetime

# Setup .env file
def create_env_file():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env_path):
        secret_key = secrets.token_hex(32)
        with open(env_path, 'w') as f:
            f.write(f"SECRET_KEY={secret_key}\n")
        print(f"Created .env file with new secret key: {secret_key}")

create_env_file()
load_dotenv()

# App configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mood_brewer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Database models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    caffeine_goal = db.Column(db.Integer, default=400)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Tracks each drink a user logs: name, caffeine amount, mood, and date.
class DrinkEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    drink_name = db.Column(db.String(100), nullable=False)
    caffeine_amount = db.Column(db.Integer, nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)

    user = db.relationship('User', backref=db.backref('drinks', lazy=True))


# Daily summary of caffeine intake and mood
class DailySummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total_caffeine = db.Column(db.Integer, nullable=False)
    average_mood = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', backref=db.backref('summaries', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home')
@login_required
def home():
    user = current_user
    caffeine_goal = user.caffeine_goal if user and user.caffeine_goal else 400

    # Get today's drinks for the current user
    today = datetime.now().date()
    drinks = DrinkEntry.query.filter_by(
        user_id=current_user.id,
        date=today
    ).all()

    # Format drinks for display
    formatted_drinks = [
        {
            "name": drink.drink_name,
            "caffeine": drink.caffeine_amount,
            "mood_color": drink.mood.lower()  # This will match our CSS classes (sleepy, tired, etc.)
        }
        for drink in drinks
    ]

    # Calculate total caffeine intake for today
    caffeine_intake = sum(drink.caffeine_amount for drink in drinks)

    return render_template("home.html",
        drinks=formatted_drinks,
        caffeine_intake=caffeine_intake,
        caffeine_goal=caffeine_goal,
        percentage=round((caffeine_intake / caffeine_goal) * 100) if caffeine_goal else 0
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('signup'))
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('signup'))
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during signup')
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('landing'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/caff_stat')
@login_required
def caff_stat():
    # Get daily summaries for the current user, ordered by date descending
    summaries = DailySummary.query.filter_by(user_id=current_user.id)\
        .order_by(DailySummary.date.desc())\
        .all()
    
    # Format the data for the template
    caffeine_data = [
        {
            "date": summary.date.strftime("%m/%d/%Y"),
            "total_mg": f"{summary.total_caffeine} MG",
            "overall_mood": summary.average_mood
        }
        for summary in summaries
    ]
    
    return render_template('caff_stat.html', caffeine_data=caffeine_data)

@app.route('/adddrink', methods=['GET', 'POST'])
@login_required
def adddrink():
    if request.method == 'POST':
        drink_name = request.form.get('drink_name')
        caffeine_amount = request.form.get('caffeine_amount')
        mood = request.form.get('mood')
        
        # Create new drink entry
        new_drink = DrinkEntry(
            user_id=current_user.id,
            drink_name=drink_name,
            caffeine_amount=caffeine_amount,
            mood=mood,
            date=datetime.now().date()
        )
        
        try:
            db.session.add(new_drink)
            db.session.commit()
            flash('Drink added successfully!')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the drink')
    
    return render_template('adddrink.html')

# Helper function to convert mood to number
def mood_to_number(mood):
    mood_map = {
        'Sleepy': 1,
        'Tired': 2,
        'Okay': 3,
        'Alive': 4,
        'Energized': 5
    }
    return mood_map.get(mood, 3)  # Default to 3 (Okay) if mood not found

# Helper function to convert number to mood
def number_to_mood(number):
    mood_map = {
        1: 'Sleepy',
        2: 'Tired',
        3: 'Okay',
        4: 'Alive',
        5: 'Energized'
    }
    return mood_map.get(number, 'Okay')  # Default to 'Okay' if number not found

@app.route('/finish_day', methods=['POST'])
@login_required
def finish_day():
    today = datetime.now().date()
    
    # Get all drinks for today
    today_drinks = DrinkEntry.query.filter_by(
        user_id=current_user.id,
        date=today
    ).all()
    
    if not today_drinks:
        flash('No drinks to summarize for today!')
        return redirect(url_for('home'))
    
    # Calculate total caffeine
    total_caffeine = sum(drink.caffeine_amount for drink in today_drinks)
    
    # Calculate average mood
    mood_numbers = [mood_to_number(drink.mood) for drink in today_drinks]
    average_mood_number = round(sum(mood_numbers) / len(mood_numbers))
    average_mood = number_to_mood(average_mood_number)
    
    # Create new daily summary
    new_summary = DailySummary(
        user_id=current_user.id,
        date=today,
        total_caffeine=total_caffeine,
        average_mood=average_mood
    )
    
    try:
        # Add the summary
        db.session.add(new_summary)
        
        # Delete today's drinks
        for drink in today_drinks:
            db.session.delete(drink)
        
        db.session.commit()
        flash('Day completed successfully!')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while completing the day')
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)