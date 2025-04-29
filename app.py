from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'secret_key'

db = SQLAlchemy(app)

#Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    caff_goal = db.Column(db.Integer, nullable=False, default=400)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home', methods=['GET', 'POST'])
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

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            return "Invalid credentials. Try again."
        
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        #Check if email already there
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already registered."

        #Creates and save new user
        new_user = User(username=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('login'))

    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    return redirect(url_for('landing'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)