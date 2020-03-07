#!/bin/bash -e
echo 'setting up static files....'
python manage.py collectstatic
echo 'making migrations...'
python manage.py makemigrations

echo 'Running migrations'
python manage.py migrate
echo 'Done running migrations'
# remove any old ones
exec python manage.py runserver 0.0.0.0:8080
