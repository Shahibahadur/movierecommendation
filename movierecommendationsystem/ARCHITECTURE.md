# System Architecture & Data Flow

## 🏗️ System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend (app.py)              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────┐      ┌────────────────────┐       │
│  │  Login Page UI     │      │  Main Recommender  │       │
│  │ ┌──────────────┐   │      │     Page UI        │       │
│  │ │ Sign Up Tab  │   │      │ ┌──────────────┐   │       │
│  │ └──────────────┘   │      │ │ Movie Select │   │       │
│  │ ┌──────────────┐   │      │ └──────────────┘   │       │
│  │ │ Login Tab    │   │      │ ┌──────────────┐   │       │
│  │ └──────────────┘   │      │ │ Get Recomend │   │       │
│  │                    │      │ └──────────────┘   │       │
│  │ Used When:         │      │ Shown When:        │       │
│  │ - First time       │      │ - logged_in = True │       │
│  │ - Not logged in    │      │                    │       │
│  └────────────────────┘      └────────────────────┘       │
│            │                           │                   │
│            └──────────┬────────────────┘                   │
│                       │                                    │
│                 ┌─────▼──────┐                             │
│                 │session_state│                            │
│                 │logged_in    │                            │
│                 │user_id      │                            │
│                 │username     │                            │
│                 └─────┬───────┘                             │
│                       │                                    │
└───────────────────────┼────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
   ┌─────────┐    ┌──────────┐   ┌──────────────┐
   │  auth.py│    │config.py │   │   app.py     │
   │         │    │          │   │              │
   │Register │    │Get DB    │   │Load models   │
   │Login    │    │Connect   │   │Fetch posters │
   │Validate │    │Init DB   │   │Recommend     │
   └────┬────┘    └────┬─────┘   └──────────────┘
        │              │
        └──────┬───────┘
               │
               ▼
        ┌─────────────────────────────────────────┐
        │    MySQL Database (movie_recommendation)│
        ├─────────────────────────────────────────┤
        │                                         │
        │  ┌──────────────────────────────────┐  │
        │  │ users table                      │  │
        │  ├──────────────────────────────────┤  │
        │  │ id (PK)                          │  │
        │  │ username (UNIQUE)                │  │
        │  │ email (UNIQUE)                   │  │
        │  │ password (hashed)                │  │
        │  │ created_at (TIMESTAMP)           │  │
        │  └──────────────────────────────────┘  │
        │                                         │
        │  ┌──────────────────────────────────┐  │
        │  │ user_preferences table           │  │
        │  ├──────────────────────────────────┤  │
        │  │ id (PK)                          │  │
        │  │ user_id (FK to users)            │  │
        │  │ favorite_genre                   │  │
        │  │ favorite_movie                   │  │
        │  │ created_at (TIMESTAMP)           │  │
        │  └──────────────────────────────────┘  │
        │                                         │
        └─────────────────────────────────────────┘
```

## 🔄 User Authentication Flow

```
START
  │
  ├─ User visits app.py
  │
  ├─ Initialize session_state
  │  ├─ logged_in = False
  │  ├─ user_id = None
  │  └─ username = None
  │
  ├─ Check: logged_in == True?
  │
  ├─ NO ──→ Show Login/Sign Up Page
  │         │
  │         ├─ New User?
  │         │  │
  │         │  └─ Sign Up Flow:
  │         │     ├─ Input validation (email, username format)
  │         │     ├─ Check duplicate username/email
  │         │     ├─ Hash password (SHA256)
  │         │     ├─ Insert into users table
  │         │     └─ Show success
  │         │
  │         └─ Existing User?
  │            │
  │            └─ Login Flow:
  │               ├─ Get username input
  │               ├─ Get password input
  │               ├─ Query: SELECT password FROM users WHERE username = ?
  │               ├─ Compare hash(input_password) == stored_password?
  │               ├─ YES → Set session_state.logged_in = True
  │               ├─        Set session_state.user_id = user_id
  │               ├─        Rerun app
  │               └─ NO → Show error message
  │
  └─ YES → Show Main Recommender Page
           │
           ├─ Display user profile (from session_state)
           ├─ Load movie_list.pkl & similarity.pkl
           ├─ Allow movie selection
           ├─ Calculate recommendations
           ├─ Fetch posters from TMDB API
           ├─ Display results
           │
           └─ Logout?
              ├─ Clear session_state
              ├─ Rerun app → Back to Login
              └─ END
```

## 🔐 Password Security

```
User Input: "password123"
        │
        ▼
    hash_password() [SHA256]
        │
        ▼
    "ef92b778bafe772564..."  (64 char hex)
        │
        ├─ Store in database ✓
        │
        ▼ (On next login)
    New Input: "password123"
        │
        ▼
    hash_password() [SHA256]
        │
        ▼
    "ef92b778bafe772564..."
        │
        ├─ Compare with stored hash
        │
        └─ Match? → Login Success ✓
```

## 📊 Input Validation Rules

```
┌─────────────┬──────────────┬──────────────────────────────┐
│ Field       │ Rule         │ Example                      │
├─────────────┼──────────────┼──────────────────────────────┤
│ Username    │ 3-20 chars   │ john_doe, user123            │
│             │ Alphanumeric │ (no spaces, special chars)   │
│             │ & underscore │                              │
├─────────────┼──────────────┼──────────────────────────────┤
│ Email       │ Valid format │ user@example.com             │
│             │ RFC standard │ NOT: user@, @example         │
├─────────────┼──────────────┼──────────────────────────────┤
│ Password    │ Min 6 chars  │ secure123, Pass@Word         │
│             │ (no format   │ (any characters allowed)     │
│             │ requirements)│                              │
└─────────────┴──────────────┴──────────────────────────────┘
```

## 🗂️ File Dependencies

```
app.py (Main)
  ├── requires: config.py (database setup)
  ├── requires: auth.py (login/register functions)
  ├── requires: movie_list.pkl (recommendation data)
  ├── requires: similarity.pkl (similarity matrix)
  └── loads: .env file (TMDB_API_KEY, DB_* credentials)

config.py
  ├── imports: mysql.connector (database driver)
  └── reads: .env file (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

auth.py
  ├── imports: mysql.connector (database driver)
  ├── imports: hashlib (password hashing)
  ├── imports: re (regex validation)
  ├── calls: config.get_db_connection()
  └── reads: .env file (indirectly via config)

requirements.txt
  ├── streamlit (web framework)
  ├── mysql-connector-python (database driver)
  ├── requests (HTTP client for TMDB API)
  ├── python-dotenv (environment variables)
  ├── pandas (data manipulation)
  ├── scikit-learn (ML/similarity)
  └── numpy, altair, etc. (utilities)
```

## 🚀 Startup Sequence

```
1. User runs: streamlit run app.py
                    │
                    ▼
2. Load environment (.env file)
                    │
                    ▼
3. Import modules (auth, config, etc.)
                    │
                    ▼
4. initialize_database() called
   ├─ Check if database exists
   ├─ Create if missing
   ├─ Create users table if missing
   └─ Create user_preferences table if missing
                    │
                    ▼
5. Initialize session_state (logged_in = False)
                    │
                    ▼
6. Check: logged_in == True?
   ├─ NO → Show login page
   └─ YES → Show recommender page
                    │
                    ▼
7. Ready for user interaction!
```

## 💾 Database Connection Pool

```
request_from_user()
          │
          ▼
    get_db_connection()
          │
          ├─ Check DB config from .env
          ├─ Establish MySQL connection
          ├─ Return connection object
          └─ Handle errors gracefully
          │
          ▼
    Execute query
          │
    ├─ auth_module: INSERT/SELECT from users
    ├─ config_module: CREATE tables
    └─ future: Store user preferences
          │
          ▼
    Close cursor & connection
          │
          ▼
    Return result to user
```

## 📈 Scalability Notes

Current setup is suitable for:
- ✅ Small to medium projects
- ✅ Development/testing
- ✅ Single server deployment

For production scaling, consider:
- 🔄 Connection pooling (DBUtils)
- 📊 Read replicas
- 🔐 SSL/TLS for database connections
- 💾 Caching layer (Redis)
- 📝 Query optimization and indexing
- 🛡️ Rate limiting
- 🔑 API authentication tokens

---

**System is production-ready for small-scale deployments!** 🚀
