import json
from django.test import TestCase
from parameterized import parameterized

from task_manager.tasks.forms import TaskForm
from task_manager.constants import TEST_DATA_FILE_FULLNAME

with open(TEST_DATA_FILE_FULLNAME) as f:
    users_data = json.load(f)


class TaskFormTestCase(TestCase):
    fixtures = ['Labels.json',
                'Users.json',
                'Statuses.json',
                'Tasks.json']

    @parameterized.expand([
                          ({'name': 'task', 'status': ''},
                           TestCase.assertFalse),

                          ({'name': '', 'status': 111},
                           TestCase.assertFalse),

                          ({'name': users_data['task_long_name'],
                            'status': 111},
                           TestCase.assertFalse),
                          ])
    def test_valid_invalid_form(self, data, func):
        form = TaskForm(data=data)
        func(self, form.is_valid())
