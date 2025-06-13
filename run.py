#!/usr/bin/env python
"""
Run script for the PayPal Clone application.
This script handles errors and provides helpful messages.
"""
import sys
import traceback
from app import create_app

def main():
    """Main function to run the application with error handling."""
    try:
        print("Starting PayPal Clone application...")
        app = create_app()
        print("Application initialized successfully!")
        print("Server will be available at: http://localhost:5000")
        app.run(host="0.0.0.0", port=5000, debug=True)
    except Exception as e:
        print("\n" + "="*50)
        print("ERROR: Failed to start the application")
        print("="*50)
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nTraceback:")
        traceback.print_exc()
        print("\nTroubleshooting tips:")
        print("1. Make sure MySQL server is running")
        print("2. Check database credentials in config.py")
        print("3. Ensure all required packages are installed: pip install -r requirements.txt")
        print("4. Try running init_db.py to initialize the database")
        print("="*50)
        sys.exit(1)

if __name__ == "__main__":
    main() 