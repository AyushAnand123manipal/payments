import os
from urllib.parse import quote_plus

# Database configuration
DB_USERNAME = 'root'
DB_PASSWORD = 'AyushAnand@123'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'paypal_clone'

# URL encode the password
encoded_password = quote_plus(DB_PASSWORD)

# Construct the database URL
DATABASE_URL = f'mysql+pymysql://{DB_USERNAME}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Flask configuration
# Use a consistent secret key for CSRF token generation
SECRET_KEY = 'paypal-clone-secret-key-2024'
DEBUG = True 