#!/bin/sh
# this script is used to boot a Docker container
pipenv run flask db init
#echo "running migrations"
#pipenv run flask db migrate
#echo "running upgrade"
#pipenv run flask db upgrade
pipenv run flask seed init
pipenv run gunicorn -w 1 -b 0.0.0.0:8000 --access-logfile - --error-logfile - main_prod:app
