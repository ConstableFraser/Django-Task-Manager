from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.user.models import User


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.fred = User.objects.create(first_name='Freddy',
                                        last_name='Mercury',
                                        username='Fred',
                                        password='superSecret#1394'
                                        )

    def test_view_page_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_signin.html')
        self.assertIn(str(_("Username")), response.content.decode('utf8'))
        self.assertIn(str(_("Password")), response.content.decode('utf8'))

    def test_view_login_valid(self):
        self.client.force_login(self.fred)
        response = self.client.get(reverse('home'))
        self.assertIn("[Freddy Mercury]", response.content.decode('utf8'))
        self.assertTemplateUsed(response, 'index.html')

    def test_view_login_invalid(self):
        User.objects.create_user(username='testuser', password='12345')
        c = Client()
        self.assertFalse(c.login(username='testuser', password='wrongpassword'))
