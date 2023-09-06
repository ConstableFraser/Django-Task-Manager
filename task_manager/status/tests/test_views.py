from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.status.models import Status
from task_manager.user.models import User
from task_manager.messages import NEED_TO_SIGNIN, STATUS_EXIST


class StatusViewTestCase(TestCase):
    fixtures = ['Status_statuses.json', 'Status_users.json']

    def setUp(self):
        self.status1 = Status.objects.get(name='Status#1')
        self.status2 = Status.objects.get(name='Status#2')
        self.fred = User.objects.get(username='Fred')

    def test_view_status_list_login_required(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 302)

    def test_status_crud_login_required(self):
        url = reverse('status_update', kwargs={"pk": self.status1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))

        url = reverse('status_delete', kwargs={"pk": self.status1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))

        url = reverse('status_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))

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
        url = reverse('status_update', kwargs={"pk": self.status1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'status/status_form.html')

    def test_view_status_valid_delete(self):
        self.client.force_login(self.fred)
        url = reverse('status_delete', kwargs={"pk": self.status1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')

    def test_view_status_update_unique(self):
        self.client.force_login(self.fred)
        url = reverse('status_update', kwargs={"pk": self.status1.id})
        response = self.client.post(url, {"name": "Status#2"})
        self.assertContains(response, _(STATUS_EXIST))
