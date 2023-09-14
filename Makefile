# Makefile
install:
	poetry install 

test:
	poetry run python manage.py test task_manager

lint:
	poetry run flake8 task_manager

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report -m
	poetry run coverage xml

start:
	poetry run python manage.py runserver

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

makemessages:
	poetry run python manage.py makemessages -l ru

compilemessages:
	poetry run python manage.py compilemessages