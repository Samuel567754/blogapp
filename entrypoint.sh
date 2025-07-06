#!/bin/bash
#!/bin/bash
set -e

echo "🛠️  Applying migrations…"
python manage.py migrate --noinput

echo "📦 Collecting static files…"
python manage.py collectstatic --noinput

exec "$@"






# #!/bin/bash
# set -e

# # Wait for Postgres (DATABASE_URL fallback)
# echo "⏳ Waiting for Postgres..."
# until psql "$DATABASE_URL" -c '\q'; do
#   sleep 1
# done
# echo "✅ Postgres is up"

# # Apply migrations & collect static
# echo "🛠️  Applying migrations…"
# python manage.py migrate --noinput

# echo "📦 Collecting static files…"
# python manage.py collectstatic --noinput

# # Execute the CMD from Dockerfile
# exec "$@"
