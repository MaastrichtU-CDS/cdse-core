#!/bin/sh

python manage.py migrate
python manage.py create_group
    python manage.py createsuperuser \
        --noinput \
        --username johan \
        --email johan@demo.com
python manage.py runserver 0.0.0.0:8000

exec "$@"
