from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here
        username = request.form.get('username')
        password = request.form.get('password')
        # For now, just redirect to home after login attempt
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/signup')
def signup():
    # Placeholder signup page
    return '<h1>Signup Page Coming Soon!</h1>'

if __name__ == '__main__':
    app.run(debug=True) 