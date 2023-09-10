from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User


class LoginViewTestCase(TestCase):
    fixtures = ['Register_users.json']

    def setUp(self):
        self.user_fred = User.objects.get(username='Fred')

    def test_view_page_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, _("Username"))
        self.assertContains(response, _("Password"))

    def test_view_login_valid(self):
        self.client.force_login(self.user_fred)
        response = self.client.get(reverse('home'))
        self.assertIn("[Freddy Mercury]", response.content.decode('utf8'))
        self.assertTemplateUsed(response, 'index.html')

    def test_view_login_invalid(self):
        User.objects.create_user(username='testuser', password='12345')
        c = Client()
        self.assertFalse(c.login(username='testuser', password='wrongpassword'))
