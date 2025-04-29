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

## Project Structure

- `app.py` - Main application file
- `config.py` - Application configuration
- `templates/` - HTML templates
- `static/` - Static files (CSS, JavaScript, images)
- `requirements.txt` - Project dependencies
- `.env` - Environment variables (automatically generated, not tracked in git)

## Security Notes

- Never commit the `.env` file to version control
- Keep your secret key secure