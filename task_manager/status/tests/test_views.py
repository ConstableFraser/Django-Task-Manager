from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.status.models import Status
from task_manager.user.models import User
from task_manager.strings import NEED_TO_SIGNIN_STR, STATUS_EXIST_STR
from task_manager.util import messages_check


class StatusViewTestCase(TestCase):
    def setUp(self):
        self.stts1 = Status.objects.create(name='Status#1')
        self.stts2 = Status.objects.create(name='Status#2')
        self.fred = User.objects.create(first_name='Freddy',
                                        last_name='Mercury',
                                        username='Fred',
                                        password='supersecret#01'
                                        )

    def test_view_status_list_login_required(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 302)

    def test_status_crud_login_required(self):
        url = reverse('status_update', kwargs={"pk": self.stts1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        cnt, msg = messages_check(self, reverse("home"))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(NEED_TO_SIGNIN_STR))

        url = reverse('status_delete', kwargs={"pk": self.stts1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        cnt, msg = messages_check(self, reverse("home"))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(NEED_TO_SIGNIN_STR))

        url = reverse('status_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        cnt, msg = messages_check(self, reverse("home"))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(NEED_TO_SIGNIN_STR))

    def test_view_status_list_signin(self):
        self.client.force_login(self.fred)
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'status/index.html')

    def test_view_status_create(self):
        self.client.force_login(self.fred)
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'status/status_form.html')

    def test_view_status_valid_update(self):
        self.client.force_login(self.fred)
        url = reverse('status_update', kwargs={"pk": self.stts1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'status/status_form.html')

    def test_view_status_valid_delete(self):
        self.client.force_login(self.fred)
        url = reverse('status_delete', kwargs={"pk": self.stts1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')

    def test_view_status_update_unique(self):
        self.client.force_login(self.fred)
        url = reverse('status_update', kwargs={"pk": self.stts1.id})
        response = self.client.post(url, {"name": "Status#2"})
        self.assertIn(str(_(STATUS_EXIST_STR)), response.content.decode('utf8'))
