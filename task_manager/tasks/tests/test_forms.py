from django.test import TestCase
from parameterized import parameterized

from task_manager.tasks.forms import TaskForm
from task_manager.statuses.models import Status
from task_manager.users.models import User


class TaskFormTestCase(TestCase):
    fixtures = ['Labels.json',
                'Users.json',
                'Statuses.json',
                'Tasks.json']

    def setUp(self):
        self.status = Status.objects.get(name='backlog')
        self.author = User.objects.get(username='JSmith')
        self.status_valid = Status.objects.get(id=500)
        self.long_name = 'eat some more of these soft French rolls \
                          and drink some tea eat some more of these \
                          soft French rolls and drink some tea eat \
                          some more of these soft French roll'

    def test_with_params(self):
        @parameterized.expand([(self.status_valid, TestCase.assertTrue),
                               ({'name': 'task', 'status': ''},
                                TestCase.assertFalse),

                               ({'name': '', 'status': 111},
                                TestCase.assertFalse),

                               ({'name': self.long_name, 'status': 111},
                                TestCase.assertFalse),
                               ])
        def test_valid_invalid_form(self, data, func):
            form = TaskForm(data=data)
            func(self, form.is_valid())
