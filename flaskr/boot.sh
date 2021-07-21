#!/bin/sh
# this script is used to boot a Docker container
#pipenv run flask db init
#pipenv run flask db migrate
#pipenv run flask db upgrade
pipenv run flask seed init
pipenv run flask run --host=0.0.0.0
