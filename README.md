# PayPal Clone

A feature-rich PayPal clone built with Flask, MySQL, and modern web technologies.

## Features

- User registration and authentication
- Secure password handling
- Send and receive money
- Add money to your account
- Transaction history
- Multi-currency support
- Profile management
- Responsive design

## Prerequisites

- Python 3.8 or higher
- MySQL server
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd payments
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up the MySQL database:
   ```
   python create_database.py
   ```

4. Initialize the database with tables and demo user:
   ```
   python init_db.py
   ```

## Configuration

The application uses the following configuration files:

- `config.py`: Contains database connection details and application settings
- `.env`: Environment variables (create this file with your settings)

Make sure to update the database credentials in `config.py` to match your MySQL setup.

## Running the Application

Start the application with:
```
python main.py
```

The application will be available at: http://localhost:5000

## Demo Account

For testing purposes, a demo account is created during initialization:
- Username: `demouser`
- Password: `password123`
- Initial balance: $1000.00

## Project Structure

- `app.py`: Main application factory
- `main.py`: Application entry point
- `models.py`: Database models
- `routes.py`: Application routes
- `forms.py`: Form definitions
- `extensions.py`: Flask extensions
- `currency_service.py`: Currency conversion service
- `templates/`: HTML templates
- `static/`: CSS, JavaScript, and other static files

## License

This project is licensed under the MIT License - see the LICENSE file for details. 