#!/usr/bin/env bash

python manage.py makemigrations wahlrechner
python manage.py migrate
python manage.py shell < docker/startup-automation.py
python manage.py runserver 0.0.0.0:80
