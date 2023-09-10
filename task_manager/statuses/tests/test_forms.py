from django.test import TestCase

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusFormTestCase(TestCase):
    def test_valid_form(self):
        data = {'name': 'status#1'}
        form = StatusForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_required_name(self):
        data = {'name': ''}
        form = StatusForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_unique_name(self):
        data = {'name': 'status#1'}
        stts = Status.objects.create(**data)
        stts.save()
        form = StatusForm(data=data)
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()
