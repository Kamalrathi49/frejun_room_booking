#!/bin/bash
set -e

# Apply migrations
python manage.py migrate

echo "Starting server..."

# Create Django superuser if specified in the environment
if [ "$DJANGO_SUPERUSER_USERNAME",  "DJANGO_SUPERUSER_EMAIL"]
then
   python manage.py createsuperuser \
       --noinput \
       --username $DJANGO_SUPERUSER_USERNAME \
       --email $DJANGO_SUPERUSER_EMAIL
fi

# Run the Django development server
echo "Starting server on 0.0.0.0:8000..."
python manage.py runserver 0.0.0.0:8000
