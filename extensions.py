from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase

# Set up SQLAlchemy with new style
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.' 