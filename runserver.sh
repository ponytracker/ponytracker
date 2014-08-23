#!/bin/bash

. env/bin/activate

cmd="python manage.py runserver"

function usage() {
  echo "Usage: $0 [default|local]"
  exit 1
}

if [[ "$#" -gt 2 ]]; then
  usage
fi

conf="$1"

if [ "$conf" == "" ]; then
  conf="default"
fi

if [ "$conf" == 'default' ]; then
  $cmd
elif [ "$conf" == 'local' ]; then
  $cmd --settings ponytracker.local_settings
else
  usage
fi
