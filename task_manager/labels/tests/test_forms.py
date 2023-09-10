from django.test import TestCase

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label


class LabelFormTestCase(TestCase):
    def test_valid_form(self):
        data = {'name': 'metka#1'}
        form = LabelForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_required_name(self):
        data = {'name': ''}
        form = LabelForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_unique_name(self):
        data = {'name': 'metka#1'}
        lbl = Label.objects.create(**data)
        lbl.save()
        form = LabelForm(data=data)
        self.assertFalse(form.is_valid())
