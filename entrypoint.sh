#!/bin/sh

echo "Applying database migrations"
python manage.py migrate

celery -A Innotwitter worker -l info --detach

echo "Creating superuser"
python manage.py createsuperuser --noinput

echo "Starting server on 0.0.0.0:8000"
python manage.py runserver 0.0.0.0:8000

