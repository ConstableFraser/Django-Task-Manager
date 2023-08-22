from django.test import TestCase
from django import forms

from ..forms import LabelForm
from ..models import Label
from ...strings import LABEL_EXIST_STR


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
