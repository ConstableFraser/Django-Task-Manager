from django.test import TestCase

from task_manager.user.models import User
from task_manager.user.forms import UserCreateForm


class UserFormTestCase(TestCase):
    def test_valid_form(self):
        data = {'first_name': 'Jonathan',
                'last_name': 'Doe',
                'username': 'JDoe',
                'password1': 'justPassword555',
                'password2': 'justPassword555'
                }
        form = UserCreateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_required_password(self):
        data = {'first_name': 'Small',
                'last_name': 'User',
                'username1': 'smUser',
                'password2': 'justPassword555'
                }
        form = UserCreateForm(data=data)
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()

    def test_invalid_form_required_password2(self):
        data = {'first_name': 'Big',
                'last_name': 'User',
                'username': 'bigUser',
                'password1': 'justPassword555'
                }
        form = UserCreateForm(data=data)
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()

    def test_invalid_form_unique_username(self):
        data = {'first_name': 'Jo',
                'last_name': 'User',
                'username': 'JDoe',
                'password': 'justPassword555'
                }
        user = User.objects.create(**data)
        user.save()
        form = UserCreateForm(data=data)
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()

    def test_invalid_form_text_username(self):
        data = {'first_name': 'Herald',
                'last_name': 'Rivia',
                'username': 'Herald777isinvalid$',
                'password1': 'justPassword555',
                'password2': 'justPassword555'
                }
        form = UserCreateForm(data=data)
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()

    def test_invalid_form_confirm_password(self):
        data = {'first_name': 'Herald',
                'last_name': 'Rivia',
                'username': 'Herald777',
                'password1': 'justPassword555',
                'password2': 'invalidpwd2'
                }
        form = UserCreateForm(data=data)
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()
