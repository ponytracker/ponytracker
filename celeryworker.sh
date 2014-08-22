#!/bin/bash

. env/bin/activate

python manage.py celery worker --loglevel=info
