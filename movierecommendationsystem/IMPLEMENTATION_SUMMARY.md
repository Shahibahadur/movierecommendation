# Movie Recommendation System - Login & Database Implementation

## ✅ What's Been Added

### 1. **Database Connection Module** (`config.py`)
- MySQL connection setup with environment variables
- Database and table auto-initialization
- Connection pooling and error handling
- Tables created:
  - `users` - stores user accounts
  - `user_preferences` - stores user favorites

### 2. **Authentication Module** (`auth.py`)
- User registration with validation
- Secure login functionality
- Password hashing (SHA256)
- Email and username validation
- User info retrieval

### 3. **Updated App** (`app.py`)
- Login/Sign Up tabs on first page
- Session-based authentication
- User profile display in sidebar
- Logout button
- Conditional page rendering (login vs recommender)

### 4. **Database Setup Files**
- `.env.example` - Configuration template
- `DATABASE_SETUP.md` - Complete setup instructions
- `schema.sql` - Manual SQL schema
- `AUTH_SETUP.md` - Authentication documentation

### 5. **Updated Dependencies** (`requirements.txt`)
- Added `mysql-connector-python` for MySQL
- Added `bcrypt` for password security

## 🚀 Quick Start

### Step 1: Install MySQL (if not already installed)
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install mysql-server

# macOS
brew install mysql

# Windows - Download from https://dev.mysql.com/downloads/mysql/
```

### Step 2: Start MySQL Service
```bash
# Ubuntu/Debian
sudo systemctl start mysql

# macOS
mysql.server start

# Windows - Should start automatically
```

### Step 3: Set Up Database
```bash
# Login to MySQL
mysql -u root -p

# Run these SQL commands:
CREATE DATABASE movie_recommendation;
CREATE USER 'movie_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON movie_recommendation.* TO 'movie_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 4: Configure Environment
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your settings:
# DB_HOST=localhost
# DB_USER=movie_user
# DB_PASSWORD=your_password
# DB_NAME=movie_recommendation
# TMDB_API_KEY=your_api_key
```

### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 6: Run Application
```bash
streamlit run app.py
```

## 📊 User Flow

```
User visits app.py
    ↓
Is user logged in? (Check session_state)
    ├─ NO → Show Login/Sign Up Page
    │   ├─ New User? → Sign Up Tab
    │   │   ├─ Enter username, email, password
    │   │   ├─ Validate inputs
    │   │   ├─ Hash password
    │   │   ├─ Store in database
    │   │   └─ Show success message
    │   │
    │   └─ Existing User? → Login Tab
    │       ├─ Enter username, password
    │       ├─ Query database
    │       ├─ Verify password hash
    │       ├─ Set session_state.logged_in = True
    │       └─ Show main page
    │
    └─ YES → Show Main Recommender Page
        ├─ Display user info in sidebar
        ├─ Show movie selector
        ├─ Show recommendations
        └─ Provide logout button
```

## 🔐 Security Features

- ✅ Password hashing (SHA256)
- ✅ Input validation (email, username format)
- ✅ SQL injection prevention (parameterized queries)
- ✅ Unique constraints (username, email)
- ✅ Session management
- ✅ Secure session state in Streamlit

## 📁 Database Schema

```
MOVIE_RECOMMENDATION
├── users
│   ├── id (PRIMARY KEY)
│   ├── username (UNIQUE)
│   ├── email (UNIQUE)
│   ├── password (HASHED)
│   └── created_at (TIMESTAMP)
│
└── user_preferences
    ├── id (PRIMARY KEY)
    ├── user_id (FOREIGN KEY)
    ├── favorite_genre
    ├── favorite_movie
    └── created_at (TIMESTAMP)
```

## 📝 File Reference

| File | Purpose |
|------|---------|
| `app.py` | Main app with login UI and recommender |
| `auth.py` | Authentication functions |
| `config.py` | Database configuration and init |
| `requirements.txt` | Python dependencies |
| `.env.example` | Configuration template |
| `schema.sql` | SQL schema (manual setup) |
| `DATABASE_SETUP.md` | Detailed setup guide |
| `AUTH_SETUP.md` | Authentication documentation |

## 🧪 Testing the System

1. Open http://localhost:8501 (Streamlit default)
2. Try signing up with new credentials
3. Verify in MySQL database:
   ```bash
   mysql -u movie_user -p
   USE movie_recommendation;
   SELECT * FROM users;
   ```
4. Log out and log back in to verify persistence
5. Use the movie recommender while logged in

## ⚠️ Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Connection refused | Check MySQL is running: `sudo systemctl status mysql` |
| Access denied | Verify credentials in `.env` file |
| Database not found | App auto-creates it, or run `schema.sql` manually |
| Username exists | Choose a different username |
| Wrong password format | Min 6 chars, no special requirements |

## 🎯 Next Steps

After setup, you can:
1. Customize the login page styling
2. Add user profile page
3. Store user movie preferences
4. Implement recommendation history
5. Add password reset functionality
6. Create admin dashboard

Enjoy your movie recommendation system! 🎬
