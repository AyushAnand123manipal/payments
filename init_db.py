from app import create_app
from extensions import db
from models import User, UserAccount, Transaction
from werkzeug.security import generate_password_hash

def init_db():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if demo user exists
        demo_user = User.query.filter_by(username='demouser').first()
        if not demo_user:
            # Create demo user
            demo_user = User(
                username='demouser',
                email='demo@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='Demo',
                last_name='User',
                preferred_currency='USD'
            )
            db.session.add(demo_user)
            db.session.commit()
            
            # Create account for demo user
            demo_account = UserAccount(
                user_id=demo_user.id,
                balance=1000.00,
                currency='USD'
            )
            db.session.add(demo_account)
            db.session.commit()
            
            print("Demo user created successfully!")
        else:
            print("Demo user already exists.")

if __name__ == "__main__":
    init_db()