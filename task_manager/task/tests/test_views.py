from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.task.models import Task
from task_manager.user.models import User
from task_manager.status.models import Status
from task_manager.messages import (NEED_TO_SIGNIN,
                                   TASK_EXIST)


class TaskViewTestCase(TestCase):
    fixtures = ['Task_labels.json',
                'Task_users.json',
                'Task_statuses.json',
                'Task_tasks.json']

    def setUp(self):
        self.status = Status.objects.get(name='Status#1')
        self.author = User.objects.get(username='Fred')
        self.task = Task.objects.get(name='Task#1')

    def test_view_task_list_login_required(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 302)

    def test_task_crud_login_required(self):
        url = reverse('task_update', kwargs={"pk": self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))

        url = reverse('task_delete', kwargs={"pk": self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))

        url = reverse('task_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('login'))
        self.assertContains(response, _(NEED_TO_SIGNIN))

    def test_view_task_list_signin(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/index.html')

    def test_view_task_create(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_form.html')

    def test_task_valid_signin(self):
        self.client.force_login(self.author)
        url = reverse('task_read', kwargs={"pk": self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_card.html')

    def test_view_task_valid_update(self):
        self.client.force_login(self.author)
        url = reverse('task_update', kwargs={"pk": self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_form.html')

    def test_view_task_valid_delete(self):
        self.client.force_login(self.author)
        url = reverse('task_delete', kwargs={"pk": self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete.html')

    def test_view_task_update_unique(self):
        self.client.force_login(self.author)
        self.task2 = Task.objects.create(name='task#2',
                                         status=self.status,
                                         author=self.author
                                         )
        self.task2.save()
        url = reverse('task_update', kwargs={"pk": self.task.id})
        response = self.client.post(url, {'name': 'task#2',
                                          'status': self.status,
                                          'author': self.author}
                                    )
        self.assertContains(response, _(TASK_EXIST))
