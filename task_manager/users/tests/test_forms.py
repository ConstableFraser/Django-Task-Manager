import json
from django.test import TestCase
from parameterized import parameterized

from task_manager.users.forms import UserCreateForm
from task_manager.constants import TEST_DATA_FILE_FULLNAME

with open(TEST_DATA_FILE_FULLNAME) as f:
    users_data = json.load(f)


class UserFormTestCase(TestCase):
    fixtures = ['Users.json']

    @parameterized.expand([(users_data['valid_user'],
                           TestCase.assertTrue,
                           False),

                           (users_data['password1_required'],
                           TestCase.assertFalse,
                           True),

                           (users_data['password2_required'],
                           TestCase.assertFalse,
                           True),

                           (users_data['username_incorrect'],
                           TestCase.assertFalse,
                           True),

                           (users_data['username_unique'],
                           TestCase.assertFalse,
                           True),

                           (users_data['confirm_password'],
                           TestCase.assertFalse,
                           True)
                           ])
    def test_form_user(self, user_data, func, commit):
        form = UserCreateForm(data=user_data)
        func(self, form.is_valid())
        if commit:
            with self.assertRaises(ValueError):
                form.save()
