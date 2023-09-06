from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.user.models import User
from task_manager.task.models import Task
from task_manager.messages import (NEED_TO_SIGNIN,
                                   USER_HAVENOT_PERMISSIONS,
                                   USER_HAS_BEEN_DELETE,
                                   USER_CANT_DELETE)


class UserViewTestCase(TestCase):
    fixtures = ['User_users.json', 'User_tasks.json']

    def setUp(self):
        self.user_fred = User.objects.get(username='Fred')
        self.user_bob = User.objects.get(username='Bob')
        self.user_billy = User.objects.get(username='Billy')
        self.task1 = Task.objects.get(name="task#1")

    def test_view_user_list(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/index.html')
        self.assertContains(response, _("Username"))
        self.assertContains(response, _("Fullname"))
        self.assertContains(response, _("Creation date"))

    def test_user_login_required_card(self):
        url = reverse('user_card', kwargs={"pk": self.user_fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))

    def test_user_login_required_update_delete(self):
        url = reverse('user_update', kwargs={"pk": self.user_fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))

        url = reverse('user_delete', kwargs={"pk": self.user_fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))

    def test_view_user_create(self):
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_form.html')
        self.assertContains(response, _("Create a user"))
        self.assertContains(response, _("Register"))

    def test_user_valid_signin(self):
        self.client.force_login(self.user_fred)
        url = reverse('user_card', kwargs={"pk": self.user_fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_detail.html')

    def test_view_user_valid_update(self):
        self.client.force_login(self.user_fred)
        url = reverse('user_update', kwargs={"pk": self.user_fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_form.html')
        self.assertContains(response, _("Update a user"))
        self.assertContains(response, _("Update"))

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

    def test_view_user_nonlogin_invalid_delete(self):
        url = reverse('user_delete', kwargs={"pk": self.user_bob.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))
