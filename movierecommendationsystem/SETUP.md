# Quick Setup Guide

## Fast Setup (5 Minutes)

### 1. Install Python
- Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"

### 2. Open Project Folder
- Navigate to the project folder in terminal/command prompt

### 3. Create Virtual Environment
```bash
python -m venv .venv
```

### 4. Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### 5. Install Packages
```bash
pip install -r requirements.txt
```

### 6. (Optional) Add API Key
Create `.env` file and add:
```
TMDB_API_KEY=your_key_here
```

### 7. Run the App
```bash
python -m streamlit run app.py
```

Done! Open http://localhost:8501 in your browser.

---

## Common Issues

**"pip not found"**
- Make sure Python is installed and added to PATH
- Try `python -m pip` instead of `pip`

**"streamlit not found"**
- Make sure virtual environment is activated (you should see `(.venv)` in terminal)
- Run `pip install -r requirements.txt` again

**Port already in use**
- Close other Streamlit apps or use: `streamlit run app.py --server.port 8502`




