from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
from dotenv import load_dotenv

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

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    
    caffeine_goal = user.caff_goal if user and user.caff_goal else 400

    #Emmie testing
    drinks = [
        {"name": "Espresso", "caffeine": 10, "mood_color": "sleepy"},
        {"name": "Latte", "caffeine": 80, "mood_color": "okay"},
        {"name": "Green Tea", "caffeine": 30, "mood_color": "energized"},
        {"name": "Celcius", "caffeine": 20, "mood_color": "alive"},
        {"name": "Brown Sugar Shaken Espresso", "caffeine": 10, "mood_color": "tired"},
        {"name": "Matcha Latte", "caffeine": 40, "mood_color": "energized"}
    ]

    caffeine_intake = sum(drink["caffeine"] for drink in drinks)
    percentage = round((caffeine_intake / caffeine_goal) * 100)

    return render_template("home.html",
        drinks=drinks,
        caffeine_intake=caffeine_intake,
        caffeine_goal=caffeine_goal,
        percentage=percentage
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
        name = request.form.get('username')
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

@app.route('/caff-stat')
@login_required
def caff_stat():
    caffeine_data = [
        {"date": "11/1/2025", "total_mg": "350 MG", "overall_mood": "Okay"},
        {"date": "11/1/2025", "total_mg": "150 MG", "overall_mood": "Alive"},
        {"date": "11/1/2025", "total_mg": "100 MG", "overall_mood": "Okay"},
        {"date": "11/1/2025", "total_mg": "400 MG", "overall_mood": "Energized"},
        {"date": "11/1/2025", "total_mg": "150 MG", "overall_mood": "Tired"},
        {"date": "11/1/2025", "total_mg": "100 MG", "overall_mood": "Sleepy"}
    ]
    return render_template('caff_stat.html', caffeine_data=caffeine_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)