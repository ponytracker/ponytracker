#!/bin/bash

. env/bin/activate

which coverage >/dev/null 2>&1
if [ "$?" -ne 0 ]; then
  pip install coverage
fi

coverage run --branch --source=accounts,permissions,tracker --omit=accounts/migrations/*.py,permissions/migrations/*.py,tracker/migrations/*.py manage.py test --settings ponytracker.test_settings
coverage report
