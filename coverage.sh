#!/bin/bash

# you must install coverage before executing this script
#   pip install coverage

. env/bin/activate

coverage run --source=issue --omit=issue/migrations/*.py manage.py test
coverage report
