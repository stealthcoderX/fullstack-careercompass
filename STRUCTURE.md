# CareerCompass - Project Structure

> Made by stealthcoderX | All rights reserved.

## 📁 Organized Folder Layout

```
CareerCompass/
│
├── frontend/                          # All client-side code (HTML, CSS, JS)
│   ├── templates/                     # Jinja2 HTML templates
│   │   ├── base.html                  # Base template (extends to all pages)
│   │   ├── auth_base.html             # Auth layout base
│   │   ├── index.html                 # Landing page
│   │   ├── register.html              # Registration page
│   │   ├── login.html                 # Login page
│   │   ├── quiz.html                  # Quiz page
│   │   ├── result.html                # Results page
│   │   └── error.html                 # Error page (404, 500, 403)
│   │
│   └── static/                        # Static assets
│       ├── css/
│       │   └── main.css               # Global stylesheet
│       │
│       └── js/
│           ├── main.js                # Global JavaScript utilities
│           ├── auth.js                # Form validation (register/login)
│           └── quiz.js                # Quiz interactions and navigation
│
├── backend/                           # All server-side code (Python Flask)
│   ├── app.py                         # Flask application factory and routes
│   ├── config.py                      # Environment config classes
│   ├── questions.py                   # Quiz questions and scoring engine
│   └── requirements.txt               # Python dependencies
│
├── database/                          # Database schemas and migrations
│   └── init.sql                       # MySQL table definitions (auto-executed on first start)
│
├── README.md                          # Original project documentation
└── STRUCTURE.md                       # This file - folder structure guide

```

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose (v2+)
- Python 3.9+ (for local development)
- MySQL 8.0+ (if running locally)

### Setup

```bash
# Navigate to the project root
cd CareerCompass

# 1. Copy environment configuration
cp .env.example .env
# Edit .env with your secrets (SECRET_KEY, DB_PASSWORD, etc.)

# 2. Start with Docker Compose (recommended)
docker compose up --build

# 3. Access the application
# http://localhost:5000
```

---

## 📂 File Organization Guide

### Frontend (`frontend/`)
**Purpose:** User interface and client-side logic

| File | Purpose |
|------|---------|
| `templates/base.html` | Base Jinja2 template with nav, footer, and block structure |
| `templates/auth_base.html` | Two-panel auth layout (register/login pages) |
| `templates/index.html` | Landing page with hero, features, and CTAs |
| `templates/register.html` | User registration form |
| `templates/login.html` | User login form |
| `templates/quiz.html` | Interactive 15-question quiz interface |
| `templates/result.html` | Career results page with scores and insights |
| `templates/error.html` | Error page (404, 403, 500) |
| `static/css/main.css` | 1200+ lines of responsive styling + animations |
| `static/js/main.js` | Global utilities (scroll animations, flash messages) |
| `static/js/auth.js` | Form validation for auth pages |
| `static/js/quiz.js` | Quiz logic, navigation, and submission handling |

### Backend (`backend/`)
**Purpose:** Server-side application logic, database models, routing

| File | Purpose |
|------|---------|
| `app.py` | Flask app factory, database models (User), all routes, error handlers, CLI commands |
| `config.py` | Configuration classes for development/production/testing environments |
| `questions.py` | Quiz question bank (15 MCQs), scoring algorithm, career data |
| `requirements.txt` | Python package dependencies (Flask, SQLAlchemy, PyMySQL, etc.) |

### Database (`database/`)
**Purpose:** Data schema and initialization

| File | Purpose |
|------|---------|
| `init.sql` | MySQL DDL for the `users` table; auto-executed by Docker on first run |

---

## 🔗 How Flask Finds Assets

The `backend/app.py` is configured to look for templates and static files in the `frontend/` folder:

```python
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_folder = os.path.join(base_dir, 'frontend', 'templates')
static_folder = os.path.join(base_dir, 'frontend', 'static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
```

This allows:
- `render_template('quiz.html')` → loads from `frontend/templates/quiz.html`
- `url_for('static', filename='js/quiz.js')` → serves from `frontend/static/js/quiz.js`

---

## 📊 Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python 3.9+, Flask, Flask-Login, Flask-SQLAlchemy |
| Database | MySQL 8.0 |
| Server | Gunicorn (production), Flask dev server (development) |
| Containerization | Docker, Docker Compose |

---

## 🛠️ Development Workflow

### Local Development (without Docker)

```bash
# 1. Setup Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Set environment variables
export APP_ENV=development
export SECRET_KEY=your-secret-key
export DB_HOST=localhost
export DB_USER=your_db_user
export DB_PASSWORD=your_db_pass
export DB_NAME=career_quiz

# 4. Run Flask dev server
cd backend
python app.py
```

### Docker Development

```bash
# Build and start all services
docker compose up --build

# Rebuild after code changes
docker compose down -v
docker compose up --build
```

---

## 📝 Notes

- Frontend templates must be in `frontend/templates/` for Flask's `render_template()` to find them
- Static assets must be in `frontend/static/` for Flask's `url_for('static', ...)` to serve them
- Backend Python modules import from each other directly (same folder)
- Database migrations require manual intervention or shell scripts; no automated ORM migrations
- All environment variables are read from `.env` at startup; changes require container restart

---

## 🚀 Deployment

See [README.md](README.md) for detailed Docker Compose setup and production deployment instructions.
