from django.test import TestCase
from parameterized import parameterized

from task_manager.users.forms import UserCreateForm


class UserFormTestCase(TestCase):
    fixtures = ['Labels.json',
                'Users.json',
                'Statuses.json',
                'Tasks.json']

    @parameterized.expand([
                          # TEST INVALID DATA
                          # checking for password2 is required
                          ({'first_name': 'Jonathan',
                            'last_name': 'Doe',
                            'username': 'JDoe',
                            'password1': 'jP*#dr5'},
                           TestCase.assertFalse,
                           True),

                          # TEST INVALID DATA
                          # checking for username is incorrect
                          ({'first_name': 'Michel',
                            'last_name': 'Arriva',
                            'username': 'mike$#',
                            'password1': 'jP*#dr5',
                            'password2': 'jP*#dr5'},
                           TestCase.assertFalse,
                           True),

                          # TEST INVALID DATA
                          # checking for password1 is required
                          ({'first_name': 'Jonathan',
                            'last_name': 'Doe',
                            'username': 'JDoe',
                            'password2': 'jP*#dr5'},
                           TestCase.assertFalse,
                           True),

                          # TEST INVALID DATA
                          # checking for username is unique
                          ({'first_name': 'Steve',
                            'last_name': 'Jobs',
                            'username': 'SteveJobs',
                            'password1': 'jP*#dr5',
                            'password2': 'jP*#dr5'},
                           TestCase.assertFalse,
                           True),

                          # TEST INVALID DATA
                          # checking for correct confirm the password
                          ({'first_name': 'Herald',
                            'last_name': 'Rivia',
                            'username': 'Herald777',
                            'password1': 'jP*#dr5',
                            'password2': 'jP*#dr542ljkw'},
                           TestCase.assertFalse,
                           True),

                          # TEST VALID DATA
                          # checking for valid form
                          ({'first_name': 'Mark',
                            'last_name': 'Fegn',
                            'username': 'Fegn',
                            'password1': 'jP*#dr5',
                            'password2': 'jP*#dr5'},
                           TestCase.assertTrue,
                           False),
                          ])
    def test_form_user(self, user_data, func, check_raise):
        form = UserCreateForm(data=user_data)
        func(self, form.is_valid())
        if check_raise:
            with self.assertRaises(ValueError):
                form.save()
