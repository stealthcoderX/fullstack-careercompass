# 🚀 Quick Start - CareerCompass

> Made by stealthcoderX | All rights reserved.

## ⚡ 3-Step Startup (Choose One)

### Option 1: Docker (Recommended - Easiest)
```bash
# 1. Make sure Docker Desktop is installed
# 2. In the project root folder, run:
docker compose up --build

Option 1: Stop containers (keep data)
docker compose down

Option 2: Stop containers AND delete all data
docker compose down -v

Option 1: Command Line 💻
mysql -h 127.0.0.1 -P 3307 -u career_user -p career_quiz
# Then enter password: career_pass
SELECT * FROM users;                    -- See all users
SELECT * FROM users WHERE predicted_career IS NOT NULL;  -- See quiz results

# 3. Open your browser to:
# http://localhost:5000
```

**What it does automatically:**
- ✅ Sets up MySQL database
- ✅ Installs Python dependencies  
- ✅ Creates database tables
- ✅ Starts Flask server

---

### Option 2: Local Python (Windows)

```bash
# 1. Navigate to backend folder
cd backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables (create .env file or set in terminal)
# For Terminal:
$env:FLASK_APP="app.py"
$env:FLASK_ENV="development"
$env:SECRET_KEY="dev-secret-key-change-in-production"
$env:DB_HOST="localhost"  # or your MySQL server
$env:DB_USER="root"
$env:DB_PASSWORD="your_password"
$env:DB_NAME="career_quiz"

# 4. Initialize database (first time only)
flask db init || python -m flask init-db

# 5. Run the app
python app.py

# 6. Open browser to:
# http://localhost:5000
```

---

### Option 3: Visual Studio Code

1. Open the project in VS Code
2. Open integrated terminal
3. Copy & paste this command:
```bash
cd backend && pip install -r requirements.txt && python app.py
```

---

## ✅ What Those Red Highlights Mean

**IMPORTANT:** The red squiggles in quiz.html and result.html are **NOT actual errors!**

They are VS Code's built-in linters (which don't understand Jinja2 templates) showing false warnings. ✓ The app will run perfectly.

When you reload VS Code or save a file, the highlights should disappear thanks to the new config files.

---

## 🔗 Available Routes

Once running, access:

| Route | Purpose |
|-------|---------|
| `http://localhost:5000/` | Landing page |
| `http://localhost:5000/register` | Create account |
| `http://localhost:5000/login` | Sign in |
| `http://localhost:5000/quiz` | Take quiz (login required) |
| `http://localhost:5000/result` | View results (login required) |
| `http://localhost:5000/health` | Health check (JSON) |

---

## 📁 Project Structure

```
CareerCompass/
├── backend/          ← Python Flask app
├── frontend/         ← HTML/CSS/JavaScript UI  
├── database/         ← MySQL schema
└── README.md         ← Full documentation
```

---

## 🐛 Troubleshooting

### "Port 5000 already in use"
```bash
# Change port in app.py or use environment variable:
$env:PORT="8000"
python app.py
```

### "Database connection error"
- Make sure MySQL is running
- Check DB_HOST, DB_USER, DB_PASSWORD in .env
- For Docker: just run `docker compose up` (handles everything)

### "Module not found" error
```bash
# Reinstall dependencies
pip install --upgrade -r backend/requirements.txt
```

### Red highlighting still showing
- Reload VS Code window: `Ctrl+Shift+P` → "Reload Window"
- Or just ignore it - it's only a display issue, doesn't affect the app

---

## ✨ That's it! Your app is ready to go! 🎉
