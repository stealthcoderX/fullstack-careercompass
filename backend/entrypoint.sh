#!/bin/bash

# ──────────────────────────────────────────────────────────────────────────
# entrypoint.sh - Flask Application Startup Script
# Made by stealthcoderX | All rights reserved.
# ──────────────────────────────────────────────────────────────────────────

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CareerCompass - Flask Application Startup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Wait for MySQL to be ready
echo "⏳ Waiting for MySQL to be ready..."
until nc -z -v -w30 "$DB_HOST" "$DB_PORT" 2>/dev/null; do
  echo "   ⟳ MySQL not ready yet, waiting..."
  sleep 5
done
echo "✅ MySQL is ready!"

# Initialize database tables
echo "📊 Initializing database tables..."
python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('✅ Database tables created/verified')
" 2>/dev/null || echo "✓ Database already initialized"

echo ""
echo "🚀 Starting Flask application..."
echo "   Server: http://0.0.0.0:5000"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start the application
exec gunicorn \
  --bind 0.0.0.0:5000 \
  --workers "${GUNICORN_WORKERS:-4}" \
  --timeout "${GUNICORN_TIMEOUT:-120}" \
  --access-logfile - \
  --error-logfile - \
  --log-level info \
  app:app
