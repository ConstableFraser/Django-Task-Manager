from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.messages import (NEED_TO_SIGNIN,
                                   STATUS_EXIST,
                                   STATUS_CREATED,
                                   STATUS_ISNOTDELETE)


class StatusViewTestCase(TestCase):
    fixtures = ['Labels.json',
                'Statuses.json',
                'Users.json',
                'Tasks.json']

    def setUp(self):
        self.status1 = Status.objects.get(name='Status#1')
        self.status2 = Status.objects.get(name='Status#2')
        self.user_fred = User.objects.get(username='Fred')


class StatusViewTestNoAuth(StatusViewTestCase):
    @parameterized.expand([reverse('status_update', kwargs={"pk": 113}),
                           reverse('status_delete', kwargs={"pk": 113}),
                           reverse('status_create'),
                           reverse('statuses')
                           ])
    def test_view_crud_no_auth(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))


class StatusViewTestCase(StatusViewTestCase):
    def test_view_status_list_signin(self):
        self.client.force_login(self.user_fred)
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/index.html')

    def test_view_status_get_create(self):
        self.client.force_login(self.user_fred)
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_view_status_create(self):
        self.client.force_login(self.user_fred)
        url = reverse('status_create')
        response = self.client.post(url, {"name": "TesingCreatingStatus"})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('statuses'))
        self.assertContains(response, _(STATUS_CREATED))

    def test_view_status_valid_update(self):
        self.client.force_login(self.user_fred)
        url = reverse('status_update', kwargs={"pk": self.status1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.client.post(url, {"name": "TestStatusName"})
        status = Status.objects.get(id=self.status1.id)
        self.assertEqual("TestStatusName", status.name)

    def test_view_status_update_unique(self):
        self.client.force_login(self.user_fred)
        url = reverse('status_update', kwargs={"pk": self.status1.id})
        response = self.client.post(url, {"name": "Status#2"})
        self.assertContains(response, _(STATUS_EXIST))

    def test_view_status_post_delete(self):
        self.client.force_login(self.user_fred)
        url = reverse('status_delete', kwargs={"pk": self.status1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')
        self.client.post(url)
        status1 = Status.objects.filter(id=self.status1.id).first()
        self.assertFalse(status1)

    def test_view_status_non_post_delete(self):
        self.client.force_login(self.user_fred)
        url = reverse('status_delete', kwargs={"pk": 110})
        self.client.post(url)
        status = Status.objects.filter(id=110).first()
        self.assertTrue(status)
        response = self.client.get(reverse('statuses'))
        self.assertContains(response, _(STATUS_ISNOTDELETE))
