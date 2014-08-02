#!/bin/bash

. env/bin/activate

python manage.py runserver 0.0.0.0:8000 --settings issuetracker.local_settings
