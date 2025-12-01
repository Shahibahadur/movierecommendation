#!/usr/bin/env python3
"""
Test script to verify MySQL database connection and setup
Run this to diagnose database issues
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test basic database connection"""
    print("Testing Database Connection...")
    print("-" * 50)
    
    try:
        import mysql.connector
        print("✓ mysql-connector-python is installed")
    except ImportError:
        print("✗ mysql-connector-python not installed")
        print("  Run: pip install mysql-connector-python")
        return False
    
    # Get database config
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'movie_recommendation')
    }
    
    print(f"\nConfiguration:")
    print(f"  Host: {db_config['host']}")
    print(f"  User: {db_config['user']}")
    print(f"  Database: {db_config['database']}")
    print(f"  Password: {'***' if db_config['password'] else '(empty)'}")
    
    # Test connection
    print("\nAttempting connection...")
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("✓ Successfully connected to MySQL database!")
            
            # Check tables
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            print(f"\nTables in database:")
            if tables:
                for table in tables:
                    print(f"  ✓ {table[0]}")
            else:
                print("  (No tables found - will be created on first run)")
            
            # Check users table structure if it exists
            try:
                cursor.execute("DESCRIBE users")
                print(f"\nUsers table columns:")
                for col in cursor.fetchall():
                    print(f"  • {col[0]} ({col[1]})")
            except:
                pass
            
            cursor.close()
            connection.close()
            return True
    except Exception as e:
        print(f"✗ Connection failed: {str(e)}")
        return False

def test_auth_module():
    """Test that auth module imports correctly"""
    print("\n\nTesting Auth Module...")
    print("-" * 50)
    
    try:
        from auth import register_user, login_user, get_user_info
        print("✓ Auth module imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import auth module: {str(e)}")
        return False

def test_config_module():
    """Test that config module imports correctly"""
    print("\n\nTesting Config Module...")
    print("-" * 50)
    
    try:
        from config import get_db_connection, initialize_database
        print("✓ Config module imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import config module: {str(e)}")
        return False

def main():
    print("\n" + "=" * 50)
    print("Movie Recommendation System - Database Test")
    print("=" * 50 + "\n")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠ WARNING: .env file not found!")
        print("  Copy .env.example to .env and configure it:")
        print("  $ cp .env.example .env")
        print()
    
    # Run tests
    results = {
        'Database Connection': test_database_connection(),
        'Config Module': test_config_module(),
        'Auth Module': test_auth_module(),
    }
    
    # Print summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    for test, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✓ All tests passed! You're ready to run the app.")
        print("  Run: streamlit run app.py")
    else:
        print("\n✗ Some tests failed. Check the errors above.")
        print("  See DATABASE_SETUP.md for troubleshooting.")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
