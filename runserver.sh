#!/bin/bash

. env/bin/activate

if [ "$1" == 'prod' ]; then
  python manage.py runserver 0.0.0.0:8000 --settings ponytracker.local_settings
else
  python manage.py runserver 0.0.0.0:8000
fi
