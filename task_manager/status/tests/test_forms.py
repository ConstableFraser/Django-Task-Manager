from django.test import TestCase
from django import forms

from ..forms import StatusForm
from ..models import Status
from ...strings import STATUS_EXIST_STR


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
