from django.test import TestCase
from parameterized import parameterized

from task_manager.statuses.forms import StatusForm


class StatusFormTestCase(TestCase):
    @parameterized.expand([('status#1', TestCase.assertTrue),
                           ('', TestCase.assertFalse),
                           ('eat some more of these soft French rolls \
                             and drink some tea eat some more of these \
                             soft French rolls and drink some tea eat \
                             some more of these soft French roll',
                            TestCase.assertFalse),
                           ])
    def test_form(self, name, func):
        form = StatusForm(data={'name': name})
        func(self, form.is_valid())
