from main import app
from extensions import db
from models import User, Transaction, UserAccount

def cleanup_database():
    with app.app_context():
        try:
            # Drop all tables
            db.drop_all()
            
            # Create all tables with new schema
            db.create_all()
            
            print("Successfully cleaned up database and recreated schema!")
            
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")

if __name__ == '__main__':
    cleanup_database() 