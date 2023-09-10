from django.test import TestCase

from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import User


class TaskFormTestCase(TestCase):
    fixtures = ['Task_labels.json',
                'Task_users.json',
                'Task_statuses.json',
                'Task_tasks.json']

    def setUp(self):
        self.status = Status.objects.get(name='backlog')
        self.author = User.objects.get(username='JSmith')
        self.status_data = {'name': 'task#1',
                            'status': self.status,
                            'author': self.author
                            }

    def test_valid_form(self):
        form = TaskForm(data=self.status_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_required_fields(self):
        data = {'name': '',
                'status': self.status
                }
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())

        data = {'name': 'task#1',
                'status': ''
                }
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_unique_name(self):
        task = Task.objects.create(**self.status_data)
        task.save()
        form = TaskForm(data=self.status_data)
        self.assertFalse(form.is_valid())
