import pymysql
# Database connection parameters
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'AyushAnand@123',
    'port': 3306
}
from werkzeug.security import generate_password_hash
def create_database():
    """
    Creates the MySQL database and tables for the PayPal clone application.
    """
    try:
        # Connect to MySQL server
        conn = pymysql.connect(**db_config)
        # Connect to MySQL server (without specifying database)
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='AyushAnand@123',
            port=3306
        )
        cursor = conn.cursor()
        
        print("Connected to MySQL successfully!")
        print("Connected to MySQL server successfully.")
        
        # Create database if it doesn't exist
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS paypal_clone")
        print("Database 'paypal_clone' created or already exists.")
        
        # Switch to the new database
        # Switch to the database
        cursor.execute("USE paypal_clone")
        print("Now using database 'paypal_clone'")
        
        # Grant privileges (if needed)
        cursor.execute("GRANT ALL PRIVILEGES ON paypal_clone.* TO 'root'@'localhost'")
        # Create tables
        # User table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(64) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password_hash VARCHAR(256) NOT NULL,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # UserAccount table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_account (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            balance FLOAT DEFAULT 0.0,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )
        """)
        
        # Transaction table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaction (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sender_id INT NOT NULL,
            receiver_id INT NOT NULL,
            amount FLOAT NOT NULL,
            description VARCHAR(200),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(20) DEFAULT 'completed',
            FOREIGN KEY (sender_id) REFERENCES user(id),
            FOREIGN KEY (receiver_id) REFERENCES user(id)
        )
        """)
        
        # Create a demo user if none exists
        cursor.execute("SELECT COUNT(*) FROM user")
        if cursor.fetchone()[0] == 0:
            # Create demo user
            password_hash = generate_password_hash('password123')
            cursor.execute(
                "INSERT INTO user (username, email, password_hash, first_name, last_name) VALUES (%s, %s, %s, %s, %s)",
                ('demouser', 'demo@example.com', password_hash, 'Demo', 'User')
            )
            
            # Get user ID
            cursor.execute("SELECT id FROM user WHERE username = 'demouser'")
            user_id = cursor.fetchone()[0]
            
            # Create user account with initial balance
            cursor.execute(
                "INSERT INTO user_account (user_id, balance) VALUES (%s, %s)",
                (user_id, 1000.0)
            )
            
            print("Demo user created with initial balance of $1000")
        
        conn.commit()
        
        print("Database setup completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
    finally:
        if 'conn' in locals() and conn:
            conn.close()