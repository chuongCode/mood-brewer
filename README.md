# Mood Brewer

A Flask web application for tracking your caffeine intake and mood.

## Setup

1. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```
   The application will automatically create a `.env` file with a secure secret key if it doesn't exist.

5. Open a web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Running Tests

To run the unit tests, make sure you have activated your virtual environment and installed the dependencies. Then run:

```
pytest
```

## Project Structure

- `app.py` - Main application file
- `config.py` - Application configuration
- `templates/` - HTML templates
- `static/` - Static files (CSS, JavaScript, images)
- `requirements.txt` - Project dependencies
- `.env` - Environment variables (automatically generated, not tracked in git)

## Navigation & Important URLs
- Landing Page (/) : Welcome screen with links to log in or sign up.
- Home Page (/home) : Displays today's drinks, caffeine intake progress bar, and options to add drinks or finish the day.
- Add Drink (/adddrink) : Form to submit a new drink entry with caffeine amount and mood.
- Profile Page (/profile) : Displays user information and allows editing of the Daily MG Goal.
- Caffeine Stats (/caff_stat) : Historical summary of caffeine intake and mood by day.
- Logout (/logout) : Ends the user session.

## Database Configurations
User Table (User)
- id : Integer, Primary Key
- username : String, unique
- email : String, unique
- password_hash : String
- caffeine_goal : Integer (default 400)

DrinkEntry Table (DrinkEntry)
- id : Integer, Primary Key
- user_id : Foreign Key, User.id
- drink_name : String
- caffeine_amount : Integer
- mood : String
- date : Date

DailySummary Table (DailySummary)
- id : Integer, Primary Key
- user_id : Foreign Key, User.id
- date : Date
- total_caffeine : Integer
- average_mood : String

## Additional Requirements
- User Authentication
- AJAX support (On Home Page.)
- Additional database interactions
- Unit tests

## Group Distribution
   - Emily: I focused mainly on designing the user interface and user experience. I also contributed to backend functionality, particularly implementing the AJAX deletion flow and database interaction logic.
   - Richard Chuong - Project Management, Application Development