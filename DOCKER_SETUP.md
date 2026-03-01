# 🐳 Docker Setup Guide - CareerCompass

> Made by stealthcoderX | All rights reserved.

Now that you have all the Docker configuration files, running the app is super easy!

---

## ✅ Prerequisites

Before running Docker, make sure you have:

1. **Docker Desktop** installed
   - Download from: https://www.docker.com/products/docker-desktop
   - Verify installation: `docker --version`

2. **Docker Compose** (usually bundled with Docker Desktop)
   - Verify: `docker compose version`

---

## 🚀 Start the Application (1 Command!)

Navigate to the project root folder and run:

```bash
docker compose up --build
```

That's it! Docker will automatically:

✅ Pull MySQL 8.0 image  
✅ Build Flask application image  
✅ Create network connection between services  
✅ Set up database volume  
✅ Initialize database tables  
✅ Start both services  

---

## 📊 What's Happening

When you run the command, you'll see output like:

```
careercompass-db  | [Server] mysqld is running as pid ...
careercompass-web | [2026-02-27 ...] Starting Flask with Gunicorn...
careercompass-web | [2026-02-27 ...] Listening on 0.0.0.0:5000
```

✅ **When you see the "Listening" message, the app is ready!**

---

## 🌐 Access Your Application

Open your browser and go to:

### **http://localhost:5000**

You'll see:
- 🏠 Landing page
- 📝 Register / Login
- 📋 Quiz
- 📊 Results

---

## 📱 API Endpoints

| URL | Purpose |
|-----|---------|
| `http://localhost:5000/` | Landing page |
| `http://localhost:5000/register` | Create account |
| `http://localhost:5000/login` | Sign in |
| `http://localhost:5000/quiz` | Take 15-question quiz |
| `http://localhost:5000/result` | View career results |
| `http://localhost:5000/health` | Health check (JSON) |

---

## 🗄️ Database Access

MySQL is running inside Docker at **localhost:3307** (mapped from 3306)

**Connection Details:**
```
Host:     localhost
Port:     3307
Database: career_quiz
User:     career_user
Password: career_pass
```

View database with GUI tools like:
- **DBeaver** (https://dbeaver.io/)
- **MySQL Workbench** (https://www.mysql.com/products/workbench/)
- **HeidiSQL** (https://www.heidisql.com/)

---

## 🛑 Stop the Application

Press `Ctrl+C` in the terminal, or in another terminal run:

```bash
docker compose down
```

---

## 🔄 Restart the Application

If you make code changes and want to restart:

```bash
# Option 1: Rebuild and restart
docker compose up --build

# Option 2: Just restart without rebuilding
docker compose restart

# Option 3: Fresh start (delete containers but keep database)
docker compose down
docker compose up

# Option 4: Fresh start (delete everything including database)
docker compose down -v
docker compose up --build
```

---

## 🔍 View Logs

```bash
# See all logs
docker compose logs -f

# See just Flask logs
docker compose logs -f web

# See just MySQL logs
docker compose logs -f db
```

---

## ⚙️ Configuration Files Explained

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Defines MySQL and Flask services |
| `backend/Dockerfile` | Instructions to build Flask image |
| `backend/entrypoint.sh` | Startup script (waits for DB, initializes tables) |
| `.env` | Environment variables (database credentials, secrets) |
| `.env.example` | Template showing all available variables |

---

## 🛠️ Troubleshooting

### ❌ "Port 5000 is already in use"
```bash
# Either stop the app using port 5000, or change the port in docker-compose.yml:
# Change:  - "5000:5000"
# To:      - "8000:5000"
# Then visit http://localhost:8000
```

### ❌ "Connection refused" when accessing http://localhost:5000
Wait 15-30 seconds. MySQL takes time to start up. Docker shows this message when ready:
```
careercompass-web | ✅ MySQL is ready!
```

### ❌ "Docker command not found"
Docker Desktop is not installed or not in PATH. Download from https://www.docker.com/products/docker-desktop

### ❌ Database errors
```bash
# Reset database and rebuild
docker compose down -v
docker compose up --build
```

### ❌ Changes to code aren't reflected
Exit the containers and rebuild:
```bash
docker compose down
docker compose up --build
```

---

## 📚 File Structure

```
CareerCompass/
├── docker-compose.yml        ← Main Docker configuration
├── .env                       ← Environment variables (used by Docker)
├── .env.example               ← Template for .env
│
├── backend/
│   ├── Dockerfile             ← How to build Flask image
│   ├── entrypoint.sh          ← Startup script
│   ├── requirements.txt        ← Python dependencies
│   ├── app.py
│   ├── config.py
│   └── questions.py
│
├── frontend/
│   ├── templates/             ← HTML files
│   └── static/                ← CSS & JavaScript
│
└── database/
    └── init.sql               ← Database schema
```

---

## ✨ Key Features of This Setup

✅ **Automatic MySQL Setup** - No manual database configuration  
✅ **Data Persistence** - Database data saved in volume (survives container restart)  
✅ **Health Checks** - Docker monitors service health  
✅ **Network Isolation** - Services communicate securely  
✅ **Scalable** - Easy to add more services (Redis, Nginx, etc.)  
✅ **Production Ready** - Uses Gunicorn, proper logging, security headers  

---

## 🎉 You're All Set!

Your application is now fully containerized and ready to run anywhere Docker is installed!

```bash
docker compose up --build
```

**That's all you need. Happy coding! 🚀**
