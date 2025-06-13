from extensions import db
from models import User, UserAccount, Transaction
import logging
import os
from sqlalchemy import inspect

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    """Initialize the database and create necessary tables"""
    try:
        # Create database directory if it doesn't exist
        db_dir = os.path.dirname('instance/paypal_clone.db')
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            logger.info(f"Created database directory: {db_dir}")

        # Create all tables
        db.create_all()
        logger.info("Database tables created successfully")

        # Get inspector to check table columns
        inspector = inspect(db.engine)

        # Check if User table exists and has required columns
        if 'user' in inspector.get_table_names():
            logger.info("User table exists")
            columns = [col['name'] for col in inspector.get_columns('user')]
            
            # Add phone column if it doesn't exist
            if 'phone' not in columns:
                with db.engine.connect() as conn:
                    conn.execute('ALTER TABLE user ADD COLUMN phone VARCHAR(15)')
                    conn.commit()
                logger.info("Added phone column to user table")

        # Check if Transaction table exists and has required columns
        if 'transaction' in inspector.get_table_names():
            logger.info("Transaction table exists")
            columns = [col['name'] for col in inspector.get_columns('transaction')]
            
            # Add currency column if it doesn't exist
            if 'currency' not in columns:
                with db.engine.connect() as conn:
                    conn.execute('ALTER TABLE transaction ADD COLUMN currency VARCHAR(3)')
                    conn.commit()
                logger.info("Added currency column to transaction table")
            
            # Add transaction_type column if it doesn't exist
            if 'transaction_type' not in columns:
                with db.engine.connect() as conn:
                    conn.execute('ALTER TABLE transaction ADD COLUMN transaction_type VARCHAR(20)')
                    conn.commit()
                logger.info("Added transaction_type column to transaction table")

        logger.info("Database setup completed successfully")
        return True

    except Exception as e:
        logger.error(f"Error setting up database: {str(e)}")
        return False

if __name__ == '__main__':
    from main import app
    with app.app_context():
        setup_database() 