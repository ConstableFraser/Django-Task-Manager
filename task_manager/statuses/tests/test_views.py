from django.test import TestCase
from django.urls import reverse
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.messages import NEED_TO_SIGNIN, STATUS_EXIST


class StatusViewTestCase(TestCase):
    fixtures = ['Status_statuses.json',
                'Status_users.json',
                'Status_tasks.json']

    def setUp(self):
        self.status1 = Status.objects.get(name='Status#1')
        self.status2 = Status.objects.get(name='Status#2')
        self.user_fred = User.objects.get(username='Fred')


class StatusViewTestNoAuth(StatusViewTestCase):
    def test_view_crud_no_auth(self):
        urls = (reverse('status_update', kwargs={"pk": self.status1.id}),
                reverse('status_delete', kwargs={"pk": self.status1.id}),
                reverse('status_create'),
                reverse('statuses'))
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            response = self.client.get(reverse('login'))
            self.assertContains(response, _(NEED_TO_SIGNIN))


class StatusViewTestCase(StatusViewTestCase):
    def test_view_status_list_signin(self):
        self.client.force_login(self.user_fred)
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'status/index.html')

    def test_view_status_get_create(self):
        self.client.force_login(self.user_fred)
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'status/status_form.html')

    def test_view_status_create(self):
        self.client.force_login(self.user_fred)
        status_data = {"name": "TesingCreatingStatus"}
        status_instance = Status.objects.create(**status_data)
        self.assertEqual("TesingCreatingStatus", status_instance.name)

    def test_view_status_valid_update(self):
        self.client.force_login(self.user_fred)
        url = reverse('status_update', kwargs={"pk": self.status1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'status/status_form.html')
        self.client.post(url, {"name": "TestStatusName"})
        status = Status.objects.get(id=self.status1.id)
        self.assertEqual("TestStatusName", status.name)

    def test_view_status_update_unique(self):
        self.client.force_login(self.user_fred)
        url = reverse('status_update', kwargs={"pk": self.status1.id})
        response = self.client.post(url, {"name": "Status#2"})
        self.assertContains(response, _(STATUS_EXIST))

    def test_view_status_valid_delete(self):
        self.client.force_login(self.user_fred)
        url = reverse('status_delete', kwargs={"pk": self.status1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')
        status = Status.objects.get(id=self.status1.id)
        self.assertTrue(status.delete())

    def test_view_status_non_delete(self):
        self.client.force_login(self.user_fred)
        status = Status.objects.get(id=110)
        with self.assertRaises(ProtectedError):
            self.assertFalse(status.delete())
