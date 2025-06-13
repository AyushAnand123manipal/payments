# PayPal Clone Application - Setup & Run Instructions

## How to Run the Application Locally

### Prerequisites
1. Python 3.8 or higher
2. MySQL server (local instance)
3. Required Python packages

### Step 1: Install Required Python Packages
```
pip install flask flask-login flask-sqlalchemy flask-wtf pymysql email-validator gunicorn
```

### Step 2: Setup the MySQL Database
First, make sure your MySQL server is running. Then create the database and tables:

```
python create_database.py
```

This script will:
- Create the `paypal_clone` database if it doesn't exist
- Create all required tables (`user`, `user_account`, `transaction`)
- Create a demo user with initial balance of $1000
  - Username: `demouser`
  - Password: `password123`

### Step 3: Configure the Database Connection
In `app.py`, make sure the MySQL connection string is correct and not commented out:

```python
# Comment this line for MySQL
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///paypal_clone.db"

# Uncomment this line for MySQL
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:AyushAnand%40123@localhost:3306/paypal_clone"
```

Note: Ensure the MySQL username, password, host, and port match your local MySQL configuration.

### Step 4: Run the Application
To start the application, run:

```
python main.py
```

The application will be available at: http://localhost:5000

## Project Structure
- `app.py`: Core Flask application setup and configuration
- `main.py`: Entry point for running the application 
- `models.py`: Database models (User, UserAccount, Transaction)
- `forms.py`: Form definitions using Flask-WTF
- `routes.py`: All application routes and view functions
- `create_database.py`: Database creation script
- `templates/`: HTML templates
- `static/`: CSS, JavaScript, and other static files

## Common Issues and Solutions

### Circular Import Errors
If you see errors like "cannot import name 'X'", this is usually due to circular imports. The application is structured to avoid this, but if it happens:

1. Make sure you're running the app using `python main.py`
2. Don't import models directly in app.py, use local imports where needed

### Database Connection Issues
If you can't connect to the database:

1. Verify MySQL server is running
2. Check username/password in connection string
3. Make sure the database name is correct
4. Ensure port 3306 is available

### CSS/JS Not Loading
If styles or JavaScript aren't working:

1. All templates should extend from base.html
2. Static file references should use url_for('static', filename='path')
3. The application must be run through Flask, not by opening HTML files directly

## Demo Account
You can log in with these credentials to test the app:
- Username: `demouser`
- Password: `password123`
- Initial balance: $1000