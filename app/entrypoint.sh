#!/bin/sh -x

python manage.py migrate --noinput || exit 1
python manage.py collectstatic --noinput --clear || exit 1
uwsgi --ini uwsgi.ini || exit 1
