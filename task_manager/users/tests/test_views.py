from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.messages import (NEED_TO_SIGNIN,
                                   USER_HAVENOT_PERMISSIONS,
                                   USER_HAS_BEEN_DELETE,
                                   USER_CANT_DELETE,
                                   USER_WAS_UPDATED,
                                   USERNAME_REQUIRED)


class UserViewTestCase(TestCase):
    fixtures = ['User_statuses.json', 'User_users.json', 'User_tasks.json']

    def setUp(self):
        self.user_fred = User.objects.get(username='Fred')
        self.user_bob = User.objects.get(username='Bob')
        self.user_billy = User.objects.get(username='Billy')
        self.task1 = Task.objects.get(name="task#1")


class UserViewTestNoAuth(UserViewTestCase):
    def test_view_user_list(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/index.html')
        self.assertContains(response, _("Username"))
        self.assertContains(response, _("Fullname"))
        self.assertContains(response, _("Creation date"))

    def test_view_user_get_create(self):
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_form.html')
        self.assertContains(response, _("Create a user"))
        self.assertContains(response, _("Register"))

    def test_view_user_create(self):
        user_data = {"first_name": "User",
                     "last_name": "Instance",
                     "username": "hexlet",
                     "password": "sec$*pwd"
                     }
        user_instance = User.objects.create_user(**user_data)
        self.assertEqual("hexlet", user_instance.username)

    def test_view_crud_no_auth(self):
        urls = (reverse('user_card', kwargs={"pk": self.user_fred.id}),
                reverse('user_update', kwargs={"pk": self.user_fred.id}),
                reverse('user_delete', kwargs={"pk": self.user_bob.id}))
        for url in urls:
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
        self.assertTemplateUsed(response, 'user/user_detail.html')

    def test_view_user_valid_get_update(self):
        self.client.force_login(self.user_fred)
        url = reverse('user_update', kwargs={"pk": self.user_fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_form.html')
        self.assertContains(response, _("Update a user"))
        self.assertContains(response, _("Update"))

    def test_view_user_valid_post_update(self):
        user_data = {"first_name": "Updated",
                     "last_name": "User_Billy",
                     "username": "user_billy",
                     "password1": "sec$*pwd",
                     "password2": "sec$*pwd"
                     }
        user_billy = User.objects.get(username='Billy')
        self.client.force_login(self.user_billy)
        url = reverse('user_update', kwargs={"pk": user_billy.id})
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(USER_WAS_UPDATED))

    def test_view_user_invalid_post_update(self):
        user_data = {"first_name": "Updated",
                     "last_name": "User_Billy",
                     "username": "%user_billy%",
                     "password1": "sec$*pwd",
                     "password2": "sec$*pwd"
                     }
        user_billy = User.objects.get(username='Billy')
        self.client.force_login(self.user_billy)
        url = reverse('user_update', kwargs={"pk": user_billy.id})
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _(USERNAME_REQUIRED))

    def test_view_user_invalid_update(self):
        self.client.force_login(self.user_fred)
        url = reverse('user_update', kwargs={"pk": self.user_bob.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('users'))
        self.assertContains(response, _(USER_HAVENOT_PERMISSIONS))

    def test_view_user_valid_delete(self):
        self.client.force_login(self.user_fred)
        url = reverse('user_delete', kwargs={"pk": self.user_fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')
        self.assertContains(response, _("Delete a user"))
        self.assertContains(response, _("Yes, delete"))

        response = self.client.post(reverse('user_delete',
                                            kwargs={"pk": self.user_fred.id}),
                                    {"pk": self.user_fred.id})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('users'))
        self.assertContains(response, _(USER_HAS_BEEN_DELETE))

    def test_view_user_invalid_delete(self):
        self.client.force_login(self.user_fred)
        url = reverse('user_delete', kwargs={"pk": self.user_bob.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

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
