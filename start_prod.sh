#!/bin/bash
python manage.py makemigrations user &&
python manage.py makemigrations contest &&
python manage.py makemigrations problem &&
python manage.py makemigrations submission &&
python manage.py makemigrations &&
python manage.py migrate &&
gunicorn --bind="0.0.0.0:5544" vcm_api.wsgi:application
