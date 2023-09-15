from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User
from task_manager.labels.models import Label
from task_manager.messages import (NEED_TO_SIGNIN,
                                   LABEL_CREATED,
                                   LABEL_EXIST,
                                   LABEL_ISNTDELETE)


class LabelViewTestCase(TestCase):
    fixtures = ['Labels.json',
                'Users.json',
                'Statuses.json',
                'Tasks.json']

    def setUp(self):
        self.label1 = Label.objects.get(name='Label#1')
        self.label2 = Label.objects.get(name='Label#2')
        self.label3 = Label.objects.get(name='Label#3')
        self.label8 = Label.objects.get(name='Label#8')
        self.label_black = Label.objects.get(name='black_metka')
        self.user_fred = User.objects.get(username='Fred')


class LabelViewTestNoAuth(LabelViewTestCase):
    @parameterized.expand([reverse('label_update', kwargs={"pk": 4}),
                           reverse('label_delete', kwargs={"pk": 4}),
                           reverse('label_create'),
                           reverse('labels')
                           ])
    def test_view_crud_no_auth(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))


class LabelViewTestWithAuth(LabelViewTestCase):
    def test_view_label_list_signin(self):
        self.client.force_login(self.user_fred)
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/index.html')
        self.assertContains(response, _("Labels"))
        self.assertContains(response, _("Name"))
        self.assertContains(response, _("Creation date"))
        self.assertContains(response, _("ID"))

    def test_view_label_get_create(self):
        self.client.force_login(self.user_fred)
        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, _("Create label"))
        self.assertContains(response, _("Create"))

    def test_view_label_create(self):
        self.client.force_login(self.user_fred)
        url = reverse('label_create')
        response = self.client.post(url, {"name": "TesingCreatingLabel"})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('labels'))
        self.assertContains(response, _(LABEL_CREATED))

    def test_view_label_valid_update(self):
        self.client.force_login(self.user_fred)
        url = reverse('label_update', kwargs={"pk": self.label1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, _("Update label"))
        self.assertContains(response, _("Update"))
        self.client.post(url, {"name": "TestLabelName"})
        label = Label.objects.get(id=self.label1.id)
        self.assertEqual("TestLabelName", label.name)

    def test_view_label_update_unique(self):
        self.client.force_login(self.user_fred)
        url = reverse('label_update', kwargs={"pk": self.label1.id})
        response = self.client.post(url, {"name": "Label#2"})
        self.assertContains(response, _(LABEL_EXIST))

    def test_view_label_get_delete(self):
        self.client.force_login(self.user_fred)
        url = reverse('label_delete', kwargs={"pk": self.label1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')
        self.assertContains(response, _("Delete label"))
        self.assertContains(response, _("Yes, delete"))

    def test_view_label_post_delete(self):
        self.client.force_login(self.user_fred)
        url = reverse('label_delete', kwargs={"pk": self.label8.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')
        self.client.post(url)
        label8 = Label.objects.filter(id=self.label8.id).first()
        self.assertFalse(label8)

    def test_view_label_post_nondelete(self):
        self.client.force_login(self.user_fred)
        url = reverse('label_delete', kwargs={"pk": self.label_black.id})
        self.client.post(url)
        response = self.client.get(reverse('labels'))
        self.assertContains(response, _(LABEL_ISNTDELETE))
