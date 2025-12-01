# Movie Recommendation System - Authentication Guide

## Overview

The Movie Recommendation System now includes a complete authentication system with user registration, login, and MySQL database integration.

## New Features

### 1. User Registration
- Create a new account with username, email, and password
- Input validation for:
  - Username (3-20 characters, alphanumeric and underscore only)
  - Email (valid email format)
  - Password (minimum 6 characters)
- Duplicate username/email prevention
- Secure password hashing using SHA256

### 2. User Login
- Secure login with username and password
- Session management using Streamlit's session_state
- User profile display in sidebar
- Logout functionality

### 3. MySQL Database Integration
- Automatic database initialization on first run
- User data persistence
- User preferences table for future enhancements

## File Structure

```
movierecommendationsystem/
├── app.py                    # Main Streamlit application with login UI
├── auth.py                   # Authentication functions (login, register)
├── config.py                 # Database configuration and initialization
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── schema.sql                # SQL schema for manual setup
├── DATABASE_SETUP.md         # Detailed database setup instructions
└── AUTH_SETUP.md             # This file
```

## New Dependencies

- `mysql-connector-python` - MySQL database driver
- `bcrypt` - Password hashing library

## How to Set Up

### Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up MySQL:**
   - Follow instructions in `DATABASE_SETUP.md`
   - Or run the SQL commands from `schema.sql` manually

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Usage

### First Time Users
1. Open the Streamlit app
2. Go to the "Sign Up" tab
3. Enter username, email, password
4. Click "Sign Up"
5. Return to "Login" tab and sign in

### Returning Users
1. Open the Streamlit app
2. Enter username and password
3. Click "Login"
4. Browse and get movie recommendations

### Logout
- Click the "🚪 Logout" button in the sidebar to log out

## Database Tables

### users
```
id (INT, Primary Key)
username (VARCHAR, Unique)
email (VARCHAR, Unique)
password (VARCHAR, SHA256 hashed)
created_at (TIMESTAMP)
```

### user_preferences
```
id (INT, Primary Key)
user_id (INT, Foreign Key to users.id)
favorite_genre (VARCHAR)
favorite_movie (VARCHAR)
created_at (TIMESTAMP)
```

## Security Features

- Password hashing using SHA256
- Input validation on all user inputs
- SQL injection prevention using parameterized queries
- Unique constraints on username and email
- Session-based authentication

## Troubleshooting

### "Database connection failed"
- Ensure MySQL is running
- Check database credentials in `.env`
- Verify MySQL service status

### "Username or email already exists"
- Choose a different username or email
- Check if you already have an account

### "Incorrect password"
- Verify you're entering the correct password
- Passwords are case-sensitive

### Streamlit reruns on login
- This is expected behavior for session updates
- The app will redirect to the main recommender page

## Future Enhancements

- Implement user preferences storage
- Add favorite movies/genres tracking
- Create personalized recommendation history
- Add password reset functionality
- Implement user profile edit page
- Add two-factor authentication
- Create admin dashboard

## Support

For issues or questions, refer to:
- `DATABASE_SETUP.md` for database troubleshooting
- Streamlit documentation: https://docs.streamlit.io
- MySQL documentation: https://dev.mysql.com/doc
