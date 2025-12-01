# MySQL Database Setup Guide

## Database Setup Instructions

### 1. Install MySQL
If you don't have MySQL installed, follow these steps:

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mysql-server
```

**On Windows:**
- Download from https://dev.mysql.com/downloads/mysql/
- Run the installer and follow the setup wizard

**On macOS:**
```bash
brew install mysql
```

### 2. Start MySQL Service

**On Ubuntu/Debian:**
```bash
sudo systemctl start mysql
```

**On Windows:**
MySQL should start automatically after installation

**On macOS:**
```bash
mysql.server start
```

### 3. Create Database User

Open MySQL command line:
```bash
mysql -u root -p
```

Create a new user and database:
```sql
CREATE DATABASE movie_recommendation;
CREATE USER 'movie_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON movie_recommendation.* TO 'movie_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your database credentials:
   ```
   DB_HOST=localhost
   DB_USER=movie_user
   DB_PASSWORD=your_secure_password
   DB_NAME=movie_recommendation
   TMDB_API_KEY=your_tmdb_api_key
   ```

### 5. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
streamlit run app.py
```

## Database Schema

The application will automatically create two tables:

### Users Table
- `id`: Primary key (auto-increment)
- `username`: Unique username
- `email`: Unique email address
- `password`: Hashed password
- `created_at`: Account creation timestamp

### User Preferences Table
- `id`: Primary key (auto-increment)
- `user_id`: Foreign key to users table
- `favorite_genre`: User's favorite movie genre
- `favorite_movie`: User's favorite movie
- `created_at`: Preference creation timestamp

## Troubleshooting

**Connection Refused Error:**
- Ensure MySQL service is running
- Check database credentials in `.env` file
- Verify MySQL is listening on localhost:3306

**Access Denied Error:**
- Verify username and password in `.env`
- Ensure user has proper permissions
- Check that MySQL is running as expected

**Database Does Not Exist:**
- The application will attempt to create it automatically
- If not, manually run the SQL commands above
