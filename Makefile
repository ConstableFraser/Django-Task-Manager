# Makefile
test:
	python manage.py test task_manager.user.tests.test_models
	python manage.py test task_manager.user.tests.test_forms
	python manage.py test task_manager.user.tests.test_views
	python manage.py test task_manager.label.tests.test_models
	python manage.py test task_manager.label.tests.test_forms
	python manage.py test task_manager.label.tests.test_views
	python manage.py test task_manager.status.tests.test_models
	python manage.py test task_manager.status.tests.test_forms
	python manage.py test task_manager.status.tests.test_views
	python manage.py test task_manager.task.tests.test_models
	python manage.py test task_manager.task.tests.test_forms
	python manage.py test task_manager.task.tests.test_views

lint:
	poetry run flake8 task_manager
