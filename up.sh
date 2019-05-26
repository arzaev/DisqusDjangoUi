#!/usr/bin/env bash

docker-compose run --rm python python manage.py makemigrations
docker-compose run --rm python python manage.py migrate
