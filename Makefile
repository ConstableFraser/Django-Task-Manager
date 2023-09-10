# Makefile
test:
	poetry run python manage.py test task_manager.tests.test_views
	poetry run python manage.py test task_manager.users.tests.test_forms
	poetry run python manage.py test task_manager.users.tests.test_views
	poetry run python manage.py test task_manager.labels.tests.test_models
	poetry run python manage.py test task_manager.labels.tests.test_forms
	poetry run python manage.py test task_manager.labels.tests.test_views
	poetry run python manage.py test task_manager.statuses.tests.test_models
	poetry run python manage.py test task_manager.statuses.tests.test_forms
	poetry run python manage.py test task_manager.statuses.tests.test_views
	poetry run python manage.py test task_manager.tasks.tests.test_models
	poetry run python manage.py test task_manager.tasks.tests.test_forms
	poetry run python manage.py test task_manager.tasks.tests.test_views

lint:
	poetry run flake8 task_manager
	poetry run flake8 task_manager/tests/
	poetry run flake8 task_manager/users/tests/
	poetry run flake8 task_manager/labels/tests/
	poetry run flake8 task_manager/statuses/tests/
	poetry run flake8 task_manager/tasks/tests/
	poetry run flake8 task_manager/settings.py

test-coverage:
	poetry run coverage run manage.py test ./task_manager/tests
	poetry run coverage run manage.py test ./task_manager/users/tests
	poetry run coverage run manage.py test ./task_manager/labels/tests
	poetry run coverage run manage.py test ./task_manager/statuses/tests
	poetry run coverage run manage.py test ./task_manager/tasks/tests
	poetry run coverage report -m --include=task_manager/* --omit=task_manager/settings.py
	poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py

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