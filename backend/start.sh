# Production-ready startup script
#!/bin/bash

set -e

echo "Starting AI Social Media Agent..."

# Wait for database to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Run migrations
echo "Running database migrations..."
python -m alembic upgrade head

echo "Starting API server..."
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
