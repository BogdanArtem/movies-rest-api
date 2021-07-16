#!/bin/sh
# this script is used to boot a Docker container
pipenv run flask db init
pipenv run flask db migrate
pipenv run flask db upgrade
pipenv run gunicorn -w 1 -b 0.0.0.0:8000 --access-logfile - --error-logfile - main:app
