"""
app.py
------
CareerCompass – Flask application entry point.
Made by stealthcoderX | All rights reserved.

Routes
------
GET       /           Landing page
GET/POST  /register   User registration
GET/POST  /login      User login
GET       /logout     Destroy session
GET       /quiz       Quiz page          [login required]
POST      /submit     Process answers    [login required]
GET       /result     Career results     [login required]
GET       /health     JSON health-check  [public]
"""

from __future__ import annotations

import json
import logging
import os
import time
from datetime import datetime

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy

from config import get_config
from questions import (
    CAREER_DESCRIPTIONS,
    CAREER_ICONS,
    CAREER_LABELS,
    CAREER_TRAITS,
    QUESTIONS,
    calculate_result,
    get_career_label,
    get_score_percentages,
)

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ── Extensions ────────────────────────────────────────────────────────────────
db            = SQLAlchemy()
login_manager = LoginManager()


# ── Database model ────────────────────────────────────────────────────────────

class User(UserMixin, db.Model):
    """Registered user stored in MySQL."""

    __tablename__ = "users"

    id               = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    name             = db.Column(db.String(100),  nullable=False)
    email            = db.Column(db.String(150),  nullable=False, unique=True, index=True)
    password_hash    = db.Column(db.String(255),  nullable=False)
    predicted_career = db.Column(db.String(100),  nullable=True,  default=None)
    score_json       = db.Column(db.Text,         nullable=True,  default=None)
    created_at       = db.Column(db.DateTime,     nullable=False, default=datetime.utcnow)

    def set_password(self, plain: str) -> None:
        """Store the raw password string without hashing (NOT recommended for production)."""
        self.password_hash = plain

    def verify_password(self, plain: str) -> bool:
        """Compare the provided password directly to the stored value."""
        return self.password_hash == plain

    def get_scores(self) -> dict[str, int]:
        if self.score_json:
            try:
                return json.loads(self.score_json)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r}>"


@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))


# ── DB startup helper ─────────────────────────────────────────────────────────

def _wait_for_db(app: Flask, retries: int = 15, delay: int = 3) -> None:
    """
    Retry connecting to MySQL until it is ready.
    Needed because the MySQL Docker container takes several seconds to initialise
    even after its port is open.
    """
    with app.app_context():
        for attempt in range(1, retries + 1):
            try:
                db.session.execute(db.text("SELECT 1"))
                db.session.remove()
                logger.info("Database ready (attempt %d/%d).", attempt, retries)
                return
            except Exception as exc:
                logger.warning(
                    "DB not ready yet (attempt %d/%d): %s – retrying in %ds…",
                    attempt, retries, exc, delay,
                )
                time.sleep(delay)
        raise RuntimeError(
            "Could not connect to MySQL after %d attempts. "
            "Check DB_HOST, DB_USER, DB_PASSWORD, DB_NAME." % retries
        )


# ── App factory ───────────────────────────────────────────────────────────────

def create_app(config_class=None) -> Flask:
    # Get the parent directory (project root) and set template/static folders
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_folder = os.path.join(base_dir, 'frontend', 'templates')
    static_folder = os.path.join(base_dir, 'frontend', 'static')
    
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view             = "login"          # type: ignore[assignment]
    login_manager.login_message          = app.config.get("LOGIN_MESSAGE", "Please log in.")
    login_manager.login_message_category = "warning"

    _register_routes(app)
    _register_error_handlers(app)
    _register_cli(app)

    return app


# ── Validation helper ─────────────────────────────────────────────────────────

def _validate_registration(form) -> list[str]:
    errors: list[str] = []
    name     = form.get("name",             "").strip()
    email    = form.get("email",            "").strip().lower()
    password = form.get("password",         "")
    confirm  = form.get("confirm_password", "")

    if not name or len(name) < 2:
        errors.append("Full name must be at least 2 characters.")
    if len(name) > 100:
        errors.append("Name is too long (max 100 characters).")
    if not email or "@" not in email or "." not in email.split("@")[-1]:
        errors.append("Please enter a valid email address.")
    if len(email) > 150:
        errors.append("Email is too long (max 150 characters).")
    if len(password) < 8:
        errors.append("Password must be at least 8 characters.")
    if len(password) > 128:
        errors.append("Password is too long (max 128 characters).")
    if password != confirm:
        errors.append("Passwords do not match.")
    return errors


# ── Routes ────────────────────────────────────────────────────────────────────

def _register_routes(app: Flask) -> None:

    # Landing
    @app.get("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("quiz"))
        return render_template("index.html")

    # Register
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("quiz"))

        if request.method == "POST":
            errors = _validate_registration(request.form)
            if errors:
                for err in errors:
                    flash(err, "error")
                return render_template("register.html")

            email = request.form.get("email", "").strip().lower()
            name  = request.form.get("name",  "").strip()

            existing = db.session.execute(
                db.select(User).where(User.email == email)
            ).scalar_one_or_none()

            if existing:
                flash("An account with that email already exists. Please sign in.", "error")
                return render_template("register.html")

            try:
                user = User(name=name, email=email)
                user.set_password(request.form.get("password", ""))
                db.session.add(user)
                db.session.commit()
                logger.info("Registered new user: %s", email)
            except Exception:
                db.session.rollback()
                logger.exception("DB error registering %s", email)
                flash("Registration failed. Please try again.", "error")
                return render_template("register.html")

            login_user(user, remember=False)
            flash(f"Welcome, {user.name.split()[0]}! Your account is ready.", "success")
            return redirect(url_for("quiz"))

        return render_template("register.html")

    # Login
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("quiz"))

        if request.method == "POST":
            email    = request.form.get("email",    "").strip().lower()
            password = request.form.get("password", "")

            if not email or not password:
                flash("Both email and password are required.", "error")
                return render_template("login.html")

            user = db.session.execute(
                db.select(User).where(User.email == email)
            ).scalar_one_or_none()

            if user is None or not user.verify_password(password):
                logger.warning("Failed login: %s", email)
                flash("Invalid email or password.", "error")
                return render_template("login.html")

            login_user(user, remember=False)
            logger.info("User logged in: %s", email)

            next_page = request.args.get("next", "")
            if next_page and next_page.startswith("/") and not next_page.startswith("//"):
                return redirect(next_page)
            return redirect(url_for("quiz"))

        return render_template("login.html")

    # Logout
    @app.get("/logout")
    @login_required
    def logout():
        logger.info("User logged out: %s", current_user.email)
        logout_user()
        flash("You have been signed out successfully.", "success")
        return redirect(url_for("login"))

    # Quiz
    @app.get("/quiz")
    @login_required
    def quiz():
        questions_data = [
            {"id": q["id"], "text": q["text"],
             "category": q["category"], "options": q["options"]}
            for q in QUESTIONS
        ]
        return render_template("quiz.html", questions=questions_data, total=len(QUESTIONS))

    # Submit
    @app.post("/submit")
    @login_required
    def submit():
        answers: dict[str, str] = {
            k: v
            for k, v in request.form.items()
            if k.startswith("q") and k[1:].isdigit() and v != ""
        }

        if not answers:
            flash("No answers submitted. Please complete the quiz.", "error")
            return redirect(url_for("quiz"))

        try:
            predicted_career, score_dict = calculate_result(answers)
        except ValueError:
            logger.warning("Scoring error for user %s", current_user.email)
            flash("Quiz submission error. Please try again.", "error")
            return redirect(url_for("quiz"))

        try:
            user = db.session.get(User, current_user.id)
            if user is None:
                flash("Session expired. Please log in again.", "warning")
                return redirect(url_for("login"))

            user.predicted_career = predicted_career
            user.score_json       = json.dumps(score_dict)
            db.session.commit()
            logger.info(
                "Quiz saved – user: %s | career: %s | scores: %s",
                user.email, predicted_career, score_dict,
            )
        except Exception:
            db.session.rollback()
            logger.exception("DB error saving quiz for user %s", current_user.id)
            flash("Could not save results. Please try again.", "error")
            return redirect(url_for("quiz"))

        return redirect(url_for("result"))

    # Result
    @app.get("/result")
    @login_required
    def result():
        user = db.session.get(User, current_user.id)
        if user is None or not user.predicted_career:
            flash("No results found. Please complete the quiz first.", "warning")
            return redirect(url_for("quiz"))

        scores      = user.get_scores()
        career_key  = user.predicted_career
        pct_scores  = get_score_percentages(scores)
        top_pct     = pct_scores.get(career_key, 0)

        sorted_scores = sorted(
            [
                {
                    "key":   k,
                    "label": CAREER_LABELS.get(k, k.title()),
                    "icon":  CAREER_ICONS.get(k, "🎯"),
                    "pct":   pct_scores.get(k, 0),
                    "raw":   scores.get(k, 0),
                }
                for k in scores
            ],
            key=lambda x: x["pct"],
            reverse=True,
        )

        return render_template(
            "result.html",
            user=user,
            career_key=career_key,
            career_label=get_career_label(career_key),
            career_icon=CAREER_ICONS.get(career_key, "🎯"),
            career_desc=CAREER_DESCRIPTIONS.get(career_key, ""),
            career_traits=CAREER_TRAITS.get(career_key, []),
            top_pct=top_pct,
            sorted_scores=sorted_scores,
        )

    # Health-check
    @app.get("/health")
    def health():
        try:
            db.session.execute(db.text("SELECT 1"))
            db_ok = True
        except Exception:
            db_ok = False
        return jsonify({
            "status": "ok" if db_ok else "degraded",
            "db":     "ok" if db_ok else "error",
        }), (200 if db_ok else 503)


# ── Error handlers ────────────────────────────────────────────────────────────

def _register_error_handlers(app: Flask) -> None:

    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", code=404, message="Page not found."), 404

    @app.errorhandler(500)
    def server_error(e):
        logger.exception("500 error: %s", e)
        return render_template("error.html", code=500, message="Internal server error."), 500

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("error.html", code=403, message="Access denied."), 403


# ── CLI commands ──────────────────────────────────────────────────────────────

def _register_cli(app: Flask) -> None:

    @app.cli.command("init-db")
    def init_db_cmd():
        """Create all database tables (safe to re-run)."""
        with app.app_context():
            db.create_all()
            print("Database tables created successfully.")

    @app.cli.command("drop-db")
    def drop_db_cmd():
        """Drop all tables – development only."""
        confirm = input("Type 'yes' to drop ALL tables: ")
        if confirm.strip().lower() == "yes":
            with app.app_context():
                db.drop_all()
                print("All tables dropped.")
        else:
            print("Aborted.")


# ── Application instance ──────────────────────────────────────────────────────

app = create_app()

if __name__ == "__main__":
    # Used for local development only (not inside Docker).
    # Docker uses entrypoint.sh → gunicorn instead.
    _wait_for_db(app)
    with app.app_context():
        db.create_all()
        logger.info("Tables verified. Starting Flask dev server.")
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=app.config.get("DEBUG", False),
    )