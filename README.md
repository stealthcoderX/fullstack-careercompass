# CareerCompass 🎯

> 🛡️ **Made by stealthcoderX** | All rights reserved.

**An AI-powered career prediction quiz application** that helps users discover their ideal career path through an intelligent 15-question assessment.

Built with **Flask**, **MySQL**, and **Docker** for easy deployment.

---

## ✨ Features

- 🎯 **Smart Career Matching** - 15 carefully crafted questions covering personality, skills, and interests
- 📊 **Interactive Quiz** - Smooth, animated quiz interface with keyboard navigation
- 📈 **Detailed Results** - Visual score breakdown across 5 career categories
- 🔐 **User Accounts** - Secure registration and login with password hashing
- 💾 **Data Persistence** - Quiz results saved to MySQL database
- 🐳 **Docker Ready** - One-command setup with Docker Compose
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🚀 **Production Ready** - Gunicorn server, environment-based config, health checks
---

## 🏗️ Project Structure

```
CareerCompass/
│
├── 📁 frontend/                          # User Interface
│   ├── templates/                        # Jinja2 HTML templates
│   │   ├── base.html                     # Base template layout
│   │   ├── auth_base.html                # Auth pages layout
│   │   ├── index.html                    # Landing page
│   │   ├── register.html                 # Registration form
│   │   ├── login.html                    # Login form
│   │   ├── quiz.html                     # Quiz interface
│   │   ├── result.html                   # Results dashboard
│   │   └── error.html                    # Error pages
│   │
│   └── static/                           # Static Assets
│       ├── css/main.css                  # Global styling
│       └── js/
│           ├── main.js                   # Global utilities
│           ├── auth.js                   # Form validation
│           └── quiz.js                   # Quiz logic
│
├── 📁 backend/                           # Server Logic
│   ├── app.py                            # Flask app factory, routes, models
│   ├── config.py                         # Environment configuration
│   ├── questions.py                      # Quiz questions & scoring engine
│   ├── requirements.txt                  # Python dependencies
│   ├── Dockerfile                        # Docker image definition
│   ├── entrypoint.sh                     # Startup script
│   └── .dockerignore                     # Docker ignore patterns
│
├── 📁 database/                          # Data Layer
│   └── init.sql                          # MySQL schema & initialization
│
├── 📄 docker-compose.yml                 # Container orchestration
├── 📄 .env                               # Environment variables
├── 📄 .env.example                       # Environment template
├── 📄 .gitignore                         # Git ignore patterns
├── 📄 README.md                          # This file
├── 📄 QUICKSTART.md                      # Quick start guide
├── 📄 DOCKER_SETUP.md                    # Docker detailed guide
└── 📄 STRUCTURE.md                       # Detailed structure documentation
```

---

## 🚀 Quick Start (3 Steps)

### **Prerequisites**
- ✅ [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running

### **Step 1: Navigate to Project**
```bash
cd "path/to/CareerCompass"
```

### **Step 2: Start the App**
```bash
docker compose up --build
```

### **Step 3: Open Browser**
**http://localhost:5000** ✅

---

## 🌐 Available Routes

| URL | Purpose | Auth |
|-----|---------|------|
| `/` | Landing page | ❌ |
| `/register` | Create account | ❌ |
| `/login` | Sign in | ❌ |
| `/quiz` | Take quiz | ✅ |
| `/result` | View results | ✅ |
| `/logout` | Sign out | ✅ |
| `/health` | Health check (JSON) | ❌ |

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Backend** | Python 3.11, Flask 3.0.3 |
| **Database** | MySQL 8.0.45 |
| **Server** | Gunicorn 22.0.0 |
| **Container** | Docker & Docker Compose |
| **ORM** | SQLAlchemy 3.1.1 |

---

## 📦 Installation

### **With Docker** (Recommended)

```bash
docker compose up --build
# Visit http://localhost:5000
```

### **Local Development** (requires MySQL)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=app.py FLASK_ENV=development
python app.py
```

---

## 🗄️ Database Connection

### **MySQL Workbench Connection**

| Field | Value |
|-------|-------|
| **Hostname** | `localhost` |
| **Port** | `3307` |
| **Username** | `career_user` |
| **Password** | `career_pass` |
| **Database** | `career_quiz` |

### **Docker Command Line**

```bash
docker exec -it careercompass-db mysql -u career_user -p -D career_quiz
# Password: career_pass
```

### **View Users**

```sql
SELECT id, name, email, predicted_career, created_at FROM users;
```

---

## 🧠 Quiz System

### **5 Career Categories**

1. 💻 **Software Engineer** - Logic, coding, systems
2. 📊 **Data Scientist** - Analytics, statistics
3. 🎨 **UX/UI Designer** - Creativity, design
4. 📈 **Product Manager** - Strategy, business
5. 🛡️ **Cybersecurity Specialist** - Security, protection

### **Scoring**

- 15 questions
- Max 45 points per category
- Results: 0-100% (capped at 99%)
- Top category = primary match

---

## 🔧 Environment Configuration

### **.env File**

```env
FLASK_ENV=development
APP_ENV=development
SECRET_KEY=your-secret-key
MYSQL_ROOT_PASSWORD=rootpassword
DB_HOST=db
DB_PORT=3306
DB_NAME=career_quiz
DB_USER=career_user
DB_PASSWORD=career_pass
GUNICORN_WORKERS=4
GUNICORN_TIMEOUT=120
PORT=5000
```

⚠️ **Never commit `.env`** - contains passwords!

---

## 🐳 Docker Commands

```bash
# Start application
docker compose up

# Rebuild and start
docker compose up --build

# Stop containers
docker compose down

# Delete database volume
docker compose down -v

# View logs
docker compose logs -f

# Execute command in container
docker exec -it careercompass-web bash
```

---

## 📚 Additional Guides

| Document | Details |
|----------|---------|
| [QUICKSTART.md](QUICKSTART.md) | 3-step startup |
| [DOCKER_SETUP.md](DOCKER_SETUP.md) | Docker detailed guide |
| [STRUCTURE.md](STRUCTURE.md) | File structure details |

---

## 🛠️ Troubleshooting

### **Port 5000 already in use**
```yaml
# Change in docker-compose.yml:
ports:
  - "8000:5000"
# Then visit http://localhost:8000
```

### **Docker not found**
- Docker Desktop not running → Start it from Applications

### **Database connection failed**
```bash
# Reset everything
docker compose down -v
docker compose up --build
```

### **MySQL container exited**
```bash
docker compose logs db
```

---

## 🚀 Deployment Checklist

- [ ] Strong `SECRET_KEY` (32+ bytes)
- [ ] Strong `DB_PASSWORD`
- [ ] `APP_ENV=production`
- [ ] HTTPS/SSL configured
- [ ] Database backups enabled
- [ ] Gunicorn workers set to `2 * CPU_COUNT + 1`

---

## 💡 Key Features Explained

### **Smart Matching Algorithm**
Each quiz answer awards points to different careers. The algorithm accumulates scores and identifies the best match.

### **Secure Authentication**
Passwords hashed using Werkzeug security. Session-based login with Flask-Login.

### **Responsive UI**
Mobile-first design with CSS animations. Works on all devices.

### **Docker Containerization**
Entire app runs in isolated containers. Portable, scalable, production-ready.

---

## 📄 License & Copyright

**© 2025 stealthcoderX. All rights reserved.**

This project is protected by copyright law. Unauthorized copying, modification, or distribution is prohibited.

For inquiries or licensing, please contact stealthcoderX.

---

**Happy career discovery!** 🚀