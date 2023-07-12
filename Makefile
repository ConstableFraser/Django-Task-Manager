# Makefile
test:
	python manage.py test task_manager.user.tests.test_models
	python manage.py test task_manager.user.tests.test_views
	python manage.py test task_manager.user.tests.test_forms

lint:
	poetry run flake8 task_manager
