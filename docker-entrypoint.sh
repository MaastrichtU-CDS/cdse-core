#!/bin/sh

if [ "$SQL_DATABASE_DJANGO" = "djangodb" ]
then
    echo "Waiting for postgres..."
      sleep 20
    echo "PostgreSQL started"
fi

python manage.py migrate --settings=core.production
python manage.py create_group --settings=core.production
python manage.py collectstatic --no-input --clear

gunicorn core.wsgi -b 0.0.0.0:8000 & python manage.py clean_container

exec "$@"
