from django.test import TestCase

from task_manager.task.forms import TaskForm
from task_manager.task.models import Task
from task_manager.status.models import Status
from task_manager.user.models import User


class TaskFormTestCase(TestCase):
    fixtures = ['Task_labels.json',
                'Task_users.json',
                'Task_statuses.json',
                'Task_tasks.json']

    def setUp(self):
        self.status = Status.objects.get(name='backlog')
        self.author = User.objects.get(username='JSmith')
        self.data = {'name': 'task#1',
                     'status': self.status,
                     'author': self.author
                     }

    def test_valid_form(self):
        form = TaskForm(data=self.data)
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
        task = Task.objects.create(**self.data)
        task.save()
        form = TaskForm(data=self.data)
        self.assertFalse(form.is_valid())
