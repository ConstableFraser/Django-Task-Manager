from django.test import TestCase
from django import forms

from ..forms import TaskForm
from ..models import Task
from ...status.models import Status
from ...user.models import User

from ...strings import TASK_EXIST_STR


class TaskFormTestCase(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name='backlog')
        self.smith = User.objects.create(first_name='John',
                                         last_name='Smith',
                                         username='JSmith',
                                         password='pwdScrt007')
        self.data = {'name': 'task#1',
                     'status': self.status,
                     'author': self.smith
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
