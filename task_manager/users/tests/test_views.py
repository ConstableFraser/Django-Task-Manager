import json
from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.constants import TEST_DATA_FILE_FULLNAME
from task_manager.messages import (NEED_TO_SIGNIN,
                                   USER_HAVENOT_PERMISSIONS,
                                   USER_HAS_BEEN_DELETE,
                                   USER_CANT_DELETE,
                                   USER_WAS_UPDATED,
                                   USER_WAS_CREATED,
                                   USER_ALREADY_EXIST)

from task_manager.constants import TEST_DATA_FILE_FULLNAME

with open(TEST_DATA_FILE_FULLNAME) as f:
    users_data = json.load(f)


class UserViewTestCase(TestCase):
    fixtures = ['Statuses.json', 'Users.json', 'Labels.json', 'Tasks.json']

    def setUp(self):
        self.user_fred = User.objects.get(username='Fred')
        self.user_bob = User.objects.get(username='Bob')
        self.user_billy = User.objects.get(username='Billy')
        self.user_len = User.objects.get(username='Len')
        self.task1 = Task.objects.get(name="task#1")


class UserViewTestNoAuth(UserViewTestCase):
    def test_view_user_list(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')
        self.assertContains(response, _("Username"))
        self.assertContains(response, _("Fullname"))
        self.assertContains(response, _("Creation date"))

    def test_view_user_get_create(self):
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, _("Create a user"))
        self.assertContains(response, _("Register"))

    def test_view_user_post_create(self):
        response = self.client.post(reverse('user_create'),
                                    users_data['user_creating'])
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(USER_WAS_CREATED))

    @parameterized.expand([reverse('user_card', kwargs={"pk": 153}),
                           reverse('user_update', kwargs={"pk": 153}),
                           reverse('user_delete', kwargs={"pk": 154})
                           ])
    def test_view_crud_no_auth(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))


class UserViewTestWithAuth(UserViewTestCase):
    def test_view_user_signin(self):
        self.client.force_login(self.user_fred)
        url = reverse('user_card', kwargs={"pk": self.user_fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_detail.html')

    def test_view_user_valid_get_update(self):
        self.client.force_login(self.user_fred)
        url = reverse('user_update', kwargs={"pk": self.user_fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, _("Update a user"))
        self.assertContains(response, _("Update"))

    @parameterized.expand([
                          (users_data['valid_user'],
                           True,
                           302,
                           USER_WAS_UPDATED),

                          (users_data['exist_user'],
                           False,
                           200,
                           USER_ALREADY_EXIST)
                          ])
    def test_view_update_user(self, user_data, redirect, status_code, message):
        user_billy = User.objects.get(username='Billy')
        self.client.force_login(self.user_billy)
        url = reverse('user_update', kwargs={"pk": user_billy.id})
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, status_code)
        if redirect:
            response = self.client.get(reverse('login'))
        self.assertContains(response, _(message))

    def test_view_user_invalid_update(self):
        self.client.force_login(self.user_fred)
        url = reverse('user_update', kwargs={"pk": self.user_bob.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('users'))
        self.assertContains(response, _(USER_HAVENOT_PERMISSIONS))

    def test_view_user_valid_delete(self):
        self.client.force_login(self.user_len)
        url = reverse('user_delete', kwargs={"pk": self.user_len.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')
        self.assertContains(response, _("Delete a user"))
        self.assertContains(response, _("Yes, delete"))

        response = self.client.post(reverse('user_delete',
                                            kwargs={"pk": self.user_len.id}),
                                    {"pk": self.user_len.id})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('users'))
        self.assertContains(response, _(USER_HAS_BEEN_DELETE))

    def test_view_user_post_nondelete(self):
        self.client.force_login(self.user_billy)
        response = self.client.post(reverse('user_delete',
                                            kwargs={"pk": self.user_billy.id}),
                                    {"pk": self.user_billy.id})
        response = self.client.get(reverse('users'))
        self.assertContains(response, _(USER_CANT_DELETE))

    def test_view_user_post_delete(self):
        self.client.force_login(self.user_bob)
        response = self.client.post(reverse('user_delete',
                                            kwargs={"pk": self.user_bob.id}),
                                    {"pk": self.user_bob.id})
        response = self.client.get(reverse('users'))
        self.assertContains(response, _(USER_HAS_BEEN_DELETE))
