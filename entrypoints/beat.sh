#!/bin/sh

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
celery -A back beat -l INFO -s back/data/celerybeat-schedule.db
