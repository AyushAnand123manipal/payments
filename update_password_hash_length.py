import pymysql
from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

def update_password_hash_length():
    try:
        # Connect to MySQL
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            port=int(DB_PORT),
            database=DB_NAME
        )
        
        with conn.cursor() as cursor:
            # Alter the password_hash column
            cursor.execute("ALTER TABLE user MODIFY COLUMN password_hash VARCHAR(2000)")
            conn.commit()
            print("Successfully updated password_hash column length to 2000")
            
    except Exception as e:
        print(f"Error updating password_hash column: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    update_password_hash_length() 