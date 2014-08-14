#!/bin/bash

# you must install coverage before executing this script
#   pip install coverage

. env/bin/activate

coverage run manage.py test
coverage report
