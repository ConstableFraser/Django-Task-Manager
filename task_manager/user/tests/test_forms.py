from django.test import TestCase

from task_manager.user.forms import UserForm
from task_manager.user.models import User


class UserFormTestCase(TestCase):
    def test_valid_form(self):
        data = {'first_name': 'Jonathan',
                'last_name': 'Doe',
                'username': 'JDoe',
                'password1': 'justPassword555',
                'password2': 'justPassword555'
                }
        form = UserForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_required_first_name(self):
        data = {'last_name': 'Wink',
                'username': 'usrnm',
                'password1': 'justPassword555',
                'password2': 'justPassword555'
                }
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_required_password(self):
        data = {'first_name': 'Small',
                'last_name': 'User',
                'username1': 'smUser',
                'password2': 'justPassword555'
                }
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_required_password2(self):
        data = {'first_name': 'Big',
                'last_name': 'User',
                'username': 'bigUser',
                'password1': 'justPassword555'
                }
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_unique_username(self):
        data = {'first_name': 'Jo',
                'last_name': 'User',
                'username': 'JDoe',
                'password': 'justPassword555'
                }
        usr = User.objects.create(**data)
        usr.save()
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_text_username(self):
        data = {'first_name': 'Herald',
                'last_name': 'Rivia',
                'username': 'Herald777isinvalid$',
                'password1': 'justPassword555',
                'password2': 'justPassword555'
                }
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_confirm_password(self):
        data = {'first_name': 'Herald',
                'last_name': 'Rivia',
                'username': 'Herald777',
                'password1': 'justPassword555',
                'password2': 'invalidpwd2'
                }
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())
