# MySQL Setup Instructions for PayPal Clone

This guide will help you set up your PayPal Clone project with MySQL on your local machine.

## Prerequisites

1. MySQL Server installed and running
2. Python 3.8+ installed
3. Required packages installed (`pip install flask flask-login flask-sqlalchemy flask-wtf pymysql`)

## Database Setup

### Step 1: Create the Database

1. Open MySQL Workbench
2. Connect to your local MySQL server
3. Run the following SQL command to create the database:

```sql
CREATE DATABASE paypal_clone;
```

### Step 2: Update Database Configuration

In your `app.py` file, uncomment the MySQL configuration line and comment out the SQLite line:

```python
# Comment this line
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///paypal_clone.db"

# Uncomment and use this line
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:AyushAnand%40123@localhost:3306/paypal_clone"
```

### Step 3: First Run with Tables Creation

Run your application to create all the tables:

```
python app.py
```

This will automatically create all the necessary tables in your MySQL database.

## Project Structure Requirements

Ensure your project structure maintains this organization:

```
your_project/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── templates/
│   ├── base.html
│   ├── index.html
│   └── other HTML templates...
├── app.py
├── models.py
├── forms.py
├── routes.py
└── main.py
```

## CSS and JavaScript References

Make sure all your HTML templates properly reference static files using Flask's `url_for`:

```html
<!-- In your HTML templates -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
```

## Running the Application

To start the application:

```
python app.py
```

The application will be available at: http://localhost:5000

## Troubleshooting

### Connection Issues
If you encounter connection issues with MySQL, verify:
1. MySQL server is running
2. Username and password are correct
3. Database name is correct
4. Special characters in password are URL encoded (@ becomes %40, etc.)

### CSS/JS Not Loading
If CSS or JS files aren't loading:
1. Ensure all files are in the correct directories
2. Check browser console for errors
3. Verify URL paths in templates
4. Clear browser cache

### Database Migration
If you need to modify the database schema:
1. Delete all tables in MySQL Workbench 
2. Run the application again to recreate tables
3. For a more sophisticated approach, consider using Flask-Migrate