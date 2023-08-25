from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.task.models import Task
from task_manager.user.models import User
from task_manager.status.models import Status
from task_manager.strings import NEED_TO_SIGNIN_STR, TASK_EXIST_STR
from task_manager.util import messages_check


class TaskViewTestCase(TestCase):
    def setUp(self):
        self.stts = Status.objects.create(name='Status#1')
        self.athr = User.objects.create(first_name='Freddy',
                                        last_name='Mercury',
                                        username='Fred',
                                        password='supersecret#01'
                                        )
        self.tsk = Task.objects.create(name='task#1',
                                       status=self.stts,
                                       author=self.athr
                                       )

    def test_view_task_list_login_required(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 302)

    def test_task_crud_login_required(self):
        url = reverse('task_update', kwargs={"pk": self.tsk.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        cnt, msg = messages_check(self, reverse("home"))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(NEED_TO_SIGNIN_STR))

        url = reverse('task_delete', kwargs={"pk": self.tsk.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        cnt, msg = messages_check(self, reverse("home"))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(NEED_TO_SIGNIN_STR))

        url = reverse('task_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        cnt, msg = messages_check(self, reverse("home"))
        self.assertEqual(cnt, 1)
        self.assertEqual(str(msg), _(NEED_TO_SIGNIN_STR))

    def test_view_task_list_signin(self):
        self.client.force_login(self.athr)
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/index.html')

    def test_view_task_create(self):
        self.client.force_login(self.athr)
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_form.html')

    def test_task_valid_signin(self):
        self.client.force_login(self.athr)
        url = reverse('task_read', kwargs={"pk": self.tsk.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_card.html')

    def test_view_task_valid_update(self):
        self.client.force_login(self.athr)
        url = reverse('task_update', kwargs={"pk": self.tsk.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_form.html')

    def test_view_task_valid_delete(self):
        self.client.force_login(self.athr)
        url = reverse('task_delete', kwargs={"pk": self.tsk.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')

    def test_view_task_update_unique(self):
        self.client.force_login(self.athr)
        self.tsk2 = Task.objects.create(name='task#2',
                                        status=self.stts,
                                        author=self.athr
                                        )
        self.tsk2.save()
        url = reverse('task_update', kwargs={"pk": self.tsk.id})
        response = self.client.post(url, {'name': 'task#2',
                                          'status': self.stts,
                                          'author': self.athr}
                                    )
        self.assertIn(str(_(TASK_EXIST_STR)), response.content.decode('utf8'))
