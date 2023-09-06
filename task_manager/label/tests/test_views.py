from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.user.models import User
from task_manager.label.models import Label
from task_manager.messages import NEED_TO_SIGNIN, LABEL_EXIST


class LabelViewTestCase(TestCase):
    fixtures = ['Label_labels.json', 'Label_users.json']

    def setUp(self):
        self.label1 = Label.objects.get(name='Label#1')
        self.label2 = Label.objects.get(name='Label#2')
        self.label3 = Label.objects.get(name='Label#3')
        self.user_fred = User.objects.get(username='Fred')

    def test_view_label_list_login_required(self):
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))

    def test_label_crud_login_required(self):
        url = reverse('label_update', kwargs={"pk": self.label1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))

        url = reverse('label_delete', kwargs={"pk": self.label1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))

        url = reverse('label_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))

    def test_view_label_list_signin(self):
        self.client.force_login(self.user_fred)
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'label/index.html')
        self.assertContains(response, _("Labels"))
        self.assertContains(response, _("Name"))
        self.assertContains(response, _("Creation date"))
        self.assertContains(response, _("ID"))

    def test_view_label_create(self):
        self.client.force_login(self.user_fred)
        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'label/label_form.html')
        self.assertContains(response, _("Create label"))
        self.assertContains(response, _("Create"))

    def test_view_label_valid_update(self):
        self.client.force_login(self.user_fred)
        url = reverse('label_update', kwargs={"pk": self.label1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'label/label_form.html')
        self.assertContains(response, _("Update label"))
        self.assertContains(response, _("Update"))

    def test_view_label_valid_delete(self):
        self.client.force_login(self.user_fred)
        url = reverse('label_delete', kwargs={"pk": self.label1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')
        self.assertContains(response, _("Delete label"))
        self.assertContains(response, _("Yes, delete"))

    def test_view_label_update_unique(self):
        self.client.force_login(self.user_fred)
        url = reverse('label_update', kwargs={"pk": self.label1.id})
        response = self.client.post(url, {"name": "Label#2"})
        self.assertContains(response, _(LABEL_EXIST))
