# Authentication Module
import mysql.connector
from mysql.connector import Error
from config import get_db_connection
import hashlib
import re

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """Validate username (3-20 characters, alphanumeric and underscore)"""
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return re.match(pattern, username) is not None

def register_user(username, email, password):
    """Register a new user"""
    try:
        # Validate inputs
        if not validate_username(username):
            return False, "Username must be 3-20 characters (alphanumeric and underscore only)"
        
        if not validate_email(email):
            return False, "Invalid email format"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        connection = get_db_connection()
        if not connection:
            return False, "Database connection failed"
        
        cursor = connection.cursor()
        
        # Check if username or email already exists
        check_query = "SELECT * FROM users WHERE username = %s OR email = %s"
        cursor.execute(check_query, (username, email))
        
        if cursor.fetchone():
            cursor.close()
            connection.close()
            return False, "Username or email already exists"
        
        # Insert new user
        hashed_password = hash_password(password)
        insert_query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (username, email, hashed_password))
        connection.commit()
        
        cursor.close()
        connection.close()
        return True, "Registration successful! Please login."
        
    except Error as e:
        return False, f"Error during registration: {str(e)}"

def login_user(username, password):
    """Authenticate user login"""
    try:
        connection = get_db_connection()
        if not connection:
            return False, None, "Database connection failed"
        
        cursor = connection.cursor()
        
        # Query user by username
        query = "SELECT id, username, password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if not user:
            return False, None, "Username not found"
        
        # Verify password
        stored_password = user[2]
        hashed_input = hash_password(password)
        
        if stored_password == hashed_input:
            return True, user[0], "Login successful!"  # Return user_id
        else:
            return False, None, "Incorrect password"
            
    except Error as e:
        return False, None, f"Error during login: {str(e)}"

def get_user_info(user_id):
    """Retrieve user information"""
    try:
        connection = get_db_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        query = "SELECT username, email, created_at FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user_info = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if user_info:
            return {
                'username': user_info[0],
                'email': user_info[1],
                'created_at': user_info[2]
            }
        return None
        
    except Error as e:
        print(f"Error retrieving user info: {str(e)}")
        return None
