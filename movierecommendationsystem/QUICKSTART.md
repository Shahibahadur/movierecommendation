# 🚀 QUICK START GUIDE - Login & MySQL Setup

## What You Now Have

✅ **Login/Registration System** - Users can create accounts and log in  
✅ **MySQL Database** - Persistent user storage  
✅ **Session Management** - Keep users logged in  
✅ **Secure Passwords** - SHA256 hashing  
✅ **Input Validation** - Email, username, password checks  

## 5-Minute Setup

### 1️⃣ Install MySQL (Choose your OS)

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install mysql-server
sudo systemctl start mysql
```

**macOS:**
```bash
brew install mysql
mysql.server start
```

**Windows:**
Download installer: https://dev.mysql.com/downloads/mysql/

### 2️⃣ Create Database

```bash
# Open MySQL
mysql -u root -p

# Copy-paste this entire block:
CREATE DATABASE movie_recommendation;
CREATE USER 'movie_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON movie_recommendation.* TO 'movie_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3️⃣ Configure App

```bash
# Go to project directory
cd /workspaces/movierecommendation/movierecommendationsystem

# Copy config template
cp .env.example .env

# Edit .env (open and replace with your values):
# DB_USER=movie_user
# DB_PASSWORD=your_password
# TMDB_API_KEY=your_tmdb_key
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Test & Run

```bash
# Test database setup
python3 test_database.py

# Run the app
streamlit run app.py
```

## 📂 New Files Created

```
config.py                    - Database setup & connection
auth.py                      - Login/Register functions
.env.example                 - Configuration template
schema.sql                   - SQL schema (if manual setup needed)
DATABASE_SETUP.md            - Detailed database guide
AUTH_SETUP.md                - Authentication documentation
IMPLEMENTATION_SUMMARY.md    - What was added & why
test_database.py             - Database connection tester
QUICKSTART.md                - This file!
```

## 🎯 Features Now Available

| Feature | File | How to Use |
|---------|------|-----------|
| **Sign Up** | app.py | Tab 1: Enter username, email, password |
| **Login** | app.py | Tab 2: Enter username & password |
| **Logout** | app.py (sidebar) | Click "🚪 Logout" button |
| **User Info** | app.py (sidebar) | Shows after login |
| **Recommendations** | app.py (main) | Same as before, now requires login |

## 🔍 Check Database

```bash
# Open MySQL
mysql -u movie_user -p movie_recommendation

# View all users
SELECT * FROM users;

# View user preferences
SELECT * FROM user_preferences;

# Exit
EXIT;
```

## ⚠️ Troubleshooting

**"Connection refused"**
```bash
# Check if MySQL is running
sudo systemctl status mysql  # Linux
mysql.server status          # macOS
```

**"Access denied for user"**
- Double-check username/password in .env
- Make sure you created the user correctly

**"Database doesn't exist"**
- App auto-creates it, or manually run schema.sql:
```bash
mysql -u root -p < schema.sql
```

**Module not found errors**
```bash
pip install mysql-connector-python
pip install -r requirements.txt
```

## 📝 Usage Example

1. Open app → http://localhost:8501
2. Click "Sign Up" tab
3. Enter:
   - Username: `john_doe`
   - Email: `john@example.com`
   - Password: `secure123`
4. Click "Sign Up"
5. Go to "Login" tab
6. Enter credentials and click "Login"
7. See your profile in sidebar
8. Use movie recommender as usual
9. Click "🚪 Logout" to exit

## 📚 Need More Info?

- **Full setup details** → `DATABASE_SETUP.md`
- **Authentication details** → `AUTH_SETUP.md`
- **Implementation details** → `IMPLEMENTATION_SUMMARY.md`
- **Code structure** → See individual files (auth.py, config.py)

## ✨ What's Next?

After everything works, you can:
- Customize login page styling
- Add user profile page
- Store movie favorites
- Add password reset
- Create admin dashboard

---

**Ready?** Run `streamlit run app.py` and start using the system! 🎬
