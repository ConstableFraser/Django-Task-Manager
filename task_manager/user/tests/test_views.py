from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.user.models import User
from task_manager.task.models import Task
from task_manager.status.models import Status
from task_manager.messages import (NEED_TO_SIGNIN,
                                   USER_HAVENOT_PERMISSIONS,
                                   USER_HAS_BEEN_DELETE,
                                   USER_CANT_DELETE)
from task_manager.util import messages_check


class UserViewTestCase(TestCase):
    fixtures = ['User_users.json', 'User_statuses.json', 'User_tasks.json']

    def setUp(self):
        self.fred = User.objects.get(username='Fred')
        self.bobby = User.objects.get(username='Bob')
        self.athr = User.objects.get(username='Billy')
        self.status = Status.objects.get(name="status#1")
        self.task = Task.objects.get(name="task#1")

    def test_view_user_list(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/index.html')
        self.assertIn(str(_("Username")), response.content.decode('utf8'))
        self.assertIn(str(_("Fullname")), response.content.decode('utf8'))
        self.assertIn(str(_("Creation date")), response.content.decode('utf8'))

    def test_user_login_required_card(self):
        url = reverse('user_card', kwargs={"pk": self.fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        cnt, msg = messages_check(self, reverse("login"))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(NEED_TO_SIGNIN))

    def test_user_login_required_update_delete(self):
        url = reverse('user_update', kwargs={"pk": self.fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        cnt, msg = messages_check(self, reverse("home"))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(NEED_TO_SIGNIN))

        url = reverse('user_delete', kwargs={"pk": self.fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        cnt, msg = messages_check(self, reverse("home"))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(NEED_TO_SIGNIN))

    def test_view_user_create(self):
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_form.html')
        self.assertIn(str(_("Create a user")), response.content.decode('utf8'))
        self.assertIn(str(_("Register")), response.content.decode('utf8'))

    def test_user_valid_signin(self):
        self.client.force_login(self.fred)
        url = reverse('user_card', kwargs={"pk": self.fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_detail.html')

    def test_view_user_valid_update(self):
        self.client.force_login(self.fred)
        url = reverse('user_update', kwargs={"pk": self.fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_form.html')
        self.assertIn(str(_("Update a user")),
                      response.content.decode('utf8'))
        self.assertIn(str(_("Update")), response.content.decode('utf8'))

    def test_view_user_invalid_update(self):
        self.client.force_login(self.fred)
        url = reverse('user_update', kwargs={"pk": self.bobby.id})
        response = self.client.get(url)
        cnt, msg = messages_check(self, reverse('users'))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(USER_HAVENOT_PERMISSIONS))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(str(_("Update a user")),
                         response.content.decode('utf8'))
        self.assertNotIn(str(_("Update")), response.content.decode('utf8'))

    def test_view_user_valid_delete(self):
        self.client.force_login(self.fred)
        url = reverse('user_delete', kwargs={"pk": self.fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')
        self.assertIn(str(_("Delete a user")), response.content.decode('utf8'))
        self.assertIn(str(_("Yes, delete")), response.content.decode('utf8'))

        response = self.client.post(reverse('user_delete',
                                            kwargs={"pk": self.fred.id}),
                                    {"pk": self.fred.id})
        self.assertEqual(response.status_code, 302)
        cnt, msg = messages_check(self, reverse('users'))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(USER_HAS_BEEN_DELETE))

    def test_view_user_invalid_delete(self):
        self.client.force_login(self.fred)
        url = reverse('user_delete', kwargs={"pk": self.bobby.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_view_user_post_nondelete(self):
        self.client.force_login(self.athr)
        self.client.post(reverse('user_delete',
                                 kwargs={"pk": self.athr.id}),
                         {"pk": self.athr.id})
        cnt, msg = messages_check(self, reverse('users'))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(USER_CANT_DELETE))

    def test_view_user_post_delete(self):
        self.client.force_login(self.bobby)
        self.client.post(reverse('user_delete',
                                 kwargs={"pk": self.bobby.id}),
                         {"pk": self.bobby.id})
        cnt, msg = messages_check(self, reverse('users'))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(USER_HAS_BEEN_DELETE))

    def test_view_user_nonlogin_invalid_delete(self):
        url = reverse('user_delete', kwargs={"pk": self.bobby.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        cnt, msg = messages_check(self, reverse("login"))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(NEED_TO_SIGNIN))
