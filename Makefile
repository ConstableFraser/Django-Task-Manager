# Makefile
test:
	poetry run python manage.py test task_manager.user.tests.test_models
	poetry run python manage.py test task_manager.user.tests.test_forms
	poetry run python manage.py test task_manager.user.tests.test_views
	poetry run python manage.py test task_manager.label.tests.test_models
	poetry run python manage.py test task_manager.label.tests.test_forms
	poetry run python manage.py test task_manager.label.tests.test_views
	poetry run python manage.py test task_manager.status.tests.test_models
	poetry run python manage.py test task_manager.status.tests.test_forms
	poetry run python manage.py test task_manager.status.tests.test_views
	poetry run python manage.py test task_manager.task.tests.test_models
	poetry run python manage.py test task_manager.task.tests.test_forms
	poetry run python manage.py test task_manager.task.tests.test_views

lint:
	poetry run flake8 task_manager

test-coverage:
	poetry run coverage run manage.py test ./task_manager/user/tests
	poetry run coverage run manage.py test ./task_manager/label/tests
	poetry run coverage run manage.py test ./task_manager/status/tests
	poetry run coverage run manage.py test ./task_manager/task/tests
