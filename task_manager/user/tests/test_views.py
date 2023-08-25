from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.user.models import User
from task_manager.strings import NEED_TO_SIGNIN_STR
from task_manager.util import messages_check


class UserViewTestCase(TestCase):
    def setUp(self):
        self.fred = User.objects.create(first_name='Freddy',
                                        last_name='Mercury',
                                        username='Fred',
                                        password='supersecret#89'
                                        )
        self.bobby = User.objects.create(first_name='Bobby',
                                         last_name='Scott',
                                         username='Bob',
                                         password='supersecret#183'
                                         )

    def test_view_user_list(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/index.html')

    def test_user_login_required(self):
        url = reverse('user_update', kwargs={"pk": self.fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        cnt, msg = messages_check(self, reverse("home"))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(NEED_TO_SIGNIN_STR))

        url = reverse('user_delete', kwargs={"pk": self.fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        cnt, msg = messages_check(self, reverse("home"))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(NEED_TO_SIGNIN_STR))

    def test_view_user_create(self):
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_form.html')

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

    def test_view_user_invalid_update(self):
        self.client.force_login(self.fred)
        url = reverse('user_update', kwargs={"pk": self.bobby.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_view_user_valid_delete(self):
        self.client.force_login(self.fred)
        url = reverse('user_delete', kwargs={"pk": self.fred.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')

    def test_view_user_invalid_delete(self):
        self.client.force_login(self.fred)
        url = reverse('user_delete', kwargs={"pk": self.bobby.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
