#!/bin/sh

set -o errexit
set -o nounset

celery -A back worker -l INFO
