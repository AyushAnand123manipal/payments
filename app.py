import os
import logging
import pymysql
import urllib.parse
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix
from config import DATABASE_URL, SECRET_KEY, DEBUG
from extensions import db, login_manager

# Register PyMySQL as MySQL driver
pymysql.install_as_MySQLdb()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def create_app():
    # Create Flask application
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 10
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = DEBUG

    # Initialize database with app
    db.init_app(app)

    # Initialize Flask-Login
    login_manager.init_app(app)

    # Add context processor for current year
    @app.context_processor
    def inject_current_year():
        return {'now': datetime.utcnow()}

    # Import models and routes AFTER all extensions are set up
    with app.app_context():
        from models import User, Transaction, UserAccount
        
        # Load user function for Flask-Login
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
        
        # Import routes after models to avoid circular imports
        from routes import register_routes
        register_routes(app)

        # Create database tables
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
