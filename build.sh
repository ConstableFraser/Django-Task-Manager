#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip

poetry install

python manage.py migrate
