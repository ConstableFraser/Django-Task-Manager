from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..models import Label
from ...user.models import User
from ...strings import NEED_TO_SIGNIN_STR, LABEL_EXIST_STR
from ...util import messages_check


class LabelViewTestCase(TestCase):
    def setUp(self):
        self.lbl1 = Label.objects.create(name='Label#1')
        self.lbl2 = Label.objects.create(name='Label#2')
        self.fred = User.objects.create(first_name='Freddy',
                                        last_name='Mercury',
                                        username='Fred',
                                        password='supersecret#89'
                                        )

    def test_view_label_list_login_required(self):
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 302)

    def test_label_crud_login_required(self):
        url = reverse('label_update', kwargs={"pk": self.lbl1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        cnt, msg = messages_check(self, reverse("home"))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(NEED_TO_SIGNIN_STR))

        url = reverse('label_delete', kwargs={"pk": self.lbl1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        cnt, msg = messages_check(self, reverse("home"))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(NEED_TO_SIGNIN_STR))

        url = reverse('label_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        cnt, msg = messages_check(self, reverse("home"))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(NEED_TO_SIGNIN_STR))

    def test_view_label_list_signin(self):
        self.client.force_login(self.fred)
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'label/index.html')

    def test_view_label_create(self):
        self.client.force_login(self.fred)
        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'label/label_form.html')

    def test_view_label_valid_update(self):
        self.client.force_login(self.fred)
        url = reverse('label_update', kwargs={"pk": self.lbl1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'label/label_form.html')

    def test_view_label_valid_delete(self):
        self.client.force_login(self.fred)
        url = reverse('label_delete', kwargs={"pk": self.lbl1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')

    def test_view_label_update_unique(self):
        self.client.force_login(self.fred)
        url = reverse('label_update', kwargs={"pk": self.lbl1.id})
        response = self.client.post(url, {"name": "Label#2"})
        self.assertIn(str(_(LABEL_EXIST_STR)), response.content.decode('utf8'))
