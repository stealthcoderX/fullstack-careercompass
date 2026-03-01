"""
config.py
---------
CareerCompass – Application configuration.
Made by stealthcoderX | All rights reserved.

All values come from environment variables.  In Docker they are injected
by docker-compose.yml (either directly or via the .env file that Compose
reads from the project root).  Locally you can use a backend/.env file.

Important: os.environ.get() is called at *class body evaluation time*, so
every variable is resolved once when the module is first imported.
"""

import os
from dotenv import load_dotenv

# Load .env only when running outside Docker (Docker injects env vars directly)
load_dotenv()


def _db_uri() -> str:
    user     = os.environ.get("DB_USER",     "career_user")
    password = os.environ.get("DB_PASSWORD", "career_pass")
    host     = os.environ.get("DB_HOST",     "db")          # "db" = Docker service name
    port     = os.environ.get("DB_PORT",     "3306")
    name     = os.environ.get("DB_NAME",     "career_quiz")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset=utf8mb4"


class Config:
    # ── Security ──────────────────────────────────────────────────────────────
    SECRET_KEY: str = os.environ.get(
        "SECRET_KEY", "change-me-generate-with-secrets-token-hex-32"
    )

    # ── Database ──────────────────────────────────────────────────────────────
    SQLALCHEMY_DATABASE_URI: str     = _db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # Connection pool tuned for Docker networking
    SQLALCHEMY_ENGINE_OPTIONS: dict = {
        "pool_recycle":  280,    # recycle before MySQL wait_timeout (8 h default)
        "pool_pre_ping": True,   # verify connection alive before each use
        "pool_size":     10,
        "max_overflow":  20,
        "connect_args":  {
            "connect_timeout": 10,   # fail fast if DB container not ready
        },
    }

    # ── Session / Cookie ──────────────────────────────────────────────────────
    SESSION_COOKIE_HTTPONLY: bool    = True
    SESSION_COOKIE_SAMESITE: str     = "Lax"
    PERMANENT_SESSION_LIFETIME: int  = 3600   # seconds

    # ── Flask-Login ───────────────────────────────────────────────────────────
    LOGIN_MESSAGE: str               = "Please log in to access the quiz."
    LOGIN_MESSAGE_CATEGORY: str      = "warning"


class DevelopmentConfig(Config):
    DEBUG: bool                 = True
    SQLALCHEMY_ECHO: bool       = False   # flip to True to print SQL
    SESSION_COOKIE_SECURE: bool = False   # HTTP ok in dev


class ProductionConfig(Config):
    DEBUG: bool                 = False
    SQLALCHEMY_ECHO: bool       = False
    SESSION_COOKIE_SECURE: bool = True    # HTTPS only in prod


class TestingConfig(Config):
    TESTING: bool                    = True
    SQLALCHEMY_DATABASE_URI: str     = "sqlite:///:memory:"
    SESSION_COOKIE_SECURE: bool      = False
    WTF_CSRF_ENABLED: bool           = False


_config_map: dict = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
    "testing":     TestingConfig,
}


def get_config():
    """Return the correct Config class based on APP_ENV (default: development)."""
    env = os.environ.get("APP_ENV", "development").lower()
    return _config_map.get(env, DevelopmentConfig)
