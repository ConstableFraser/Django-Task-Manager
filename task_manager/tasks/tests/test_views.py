from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Task
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.messages import (NEED_TO_SIGNIN,
                                   TASK_EXIST,
                                   TASK_CREATED,
                                   TASK_UPDATED,
                                   TASK_DELETED,
                                   TASK_NON_AUTHOR)


class TaskViewTestCase(TestCase):
    fixtures = ['Labels.json',
                'Users.json',
                'Statuses.json',
                'Tasks.json']

    def setUp(self):
        self.status = Status.objects.get(name='Status#1')
        self.user_fred = User.objects.get(username='Fred')
        self.task = Task.objects.get(name='Task#299')


class TaskViewTestNoAuth(TaskViewTestCase):
    @parameterized.expand([reverse('task_update', kwargs={"pk": 299}),
                           reverse('task_delete', kwargs={"pk": 299}),
                           reverse('task_create'),
                           reverse('tasks')
                           ])
    def test_view_crud_no_auth(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))


class TaskViewTestWithAuth(TaskViewTestCase):
    def test_view_task_list_signin(self):
        self.client.force_login(self.user_fred)
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')

    def test_view_task_get_create(self):
        self.client.force_login(self.user_fred)
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_view_task_create(self):
        self.client.force_login(self.user_fred)
        url = reverse('task_create')
        task_data = {"name": "TestTaskName934",
                     "status": self.status.id,
                     "author": self.user_fred.id,
                     "created_at": "2023-08-10 11:16:09.184106+03:00"
                     }
        response = self.client.post(url, task_data)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('tasks'))
        self.assertContains(response, _(TASK_CREATED))

    def test_view_task_valid_card(self):
        self.client.force_login(self.user_fred)
        url = reverse('task_read', kwargs={"pk": self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_card.html')

    def test_view_task_valid_update(self):
        self.client.force_login(self.user_fred)
        url = reverse('task_update', kwargs={"pk": self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        response = self.client.post(url,
                                    {"name": "NewNameOfTask",
                                     "status": self.status.id,
                                     "author": self.user_fred.id})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('tasks'))
        self.assertContains(response, _(TASK_UPDATED))

    def test_view_task_update_unique(self):
        self.client.force_login(self.user_fred)
        url = reverse('task_update', kwargs={"pk": self.task.id})
        response = self.client.post(url, {'name': 'Nothing to do',
                                          'status': self.status,
                                          'author': self.user_fred}
                                    )
        self.assertContains(response, _(TASK_EXIST))

    def test_view_task_valid_delete(self):
        self.client.force_login(self.user_fred)
        url = reverse('task_delete', kwargs={"pk": self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('tasks'))
        self.assertContains(response, _(TASK_DELETED))

    def test_view_task_non_delete(self):
        url = reverse('task_delete', kwargs={"pk": self.task.id})
        user_gubin = User.objects.get(username='AGubin')
        self.client.force_login(user_gubin)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('tasks'))
        self.assertContains(response, _(TASK_NON_AUTHOR))
