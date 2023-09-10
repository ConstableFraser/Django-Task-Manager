from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Task
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.messages import (NEED_TO_SIGNIN,
                                   TASK_EXIST,
                                   TASK_NON_AUTHOR)


class TaskViewTestCase(TestCase):
    fixtures = ['Task_labels.json',
                'Task_users.json',
                'Task_statuses.json',
                'Task_tasks.json']

    def setUp(self):
        self.status = Status.objects.get(name='Status#1')
        self.user_fred = User.objects.get(username='Fred')
        self.task = Task.objects.get(name='Task#1')


class TaskViewTestNoAuth(TaskViewTestCase):
    def test_view_crud_no_auth(self):
        urls = (reverse('task_update', kwargs={"pk": self.task.id}),
                reverse('task_delete', kwargs={"pk": self.task.id}),
                reverse('task_create'),
                reverse('tasks'))
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            response = self.client.get(reverse('login'))
            self.assertContains(response, _(NEED_TO_SIGNIN))


class TaskViewTestWithAuth(TaskViewTestCase):
    def test_view_task_list_signin(self):
        self.client.force_login(self.user_fred)
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/index.html')

    def test_view_task_get_create(self):
        self.client.force_login(self.user_fred)
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_form.html')

    def test_view_task_create(self):
        self.client.force_login(self.user_fred)
        task_data = {'name': 'TestTaskCreating',
                     'status': self.status,
                     'author': self.user_fred
                     }
        task_instance = Task.objects.create(**task_data)
        self.assertEqual("TestTaskCreating", task_instance.name)

    def test_view_task_valid_card(self):
        self.client.force_login(self.user_fred)
        url = reverse('task_read', kwargs={"pk": self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_card.html')

    def test_view_task_valid_update(self):
        self.client.force_login(self.user_fred)
        url = reverse('task_update', kwargs={"pk": self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_form.html')
        task = Task.objects.get(id=self.task.id)
        task.name = "TestTaskName"
        task.save()
        self.assertEqual("TestTaskName", task.name)

    def test_view_task_update_unique(self):
        self.client.force_login(self.user_fred)
        self.task2 = Task.objects.create(name='task#2',
                                         status=self.status,
                                         author=self.user_fred
                                         )
        self.task2.save()
        url = reverse('task_update', kwargs={"pk": self.task.id})
        response = self.client.post(url, {'name': 'task#2',
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
        task = Task.objects.get(id=self.task.id)
        self.assertTrue(task.delete())

    def test_view_task_non_delete(self):
        url = reverse('task_delete', kwargs={"pk": self.task.id})
        user_gubin = User.objects.get(username='AGubin')
        self.client.force_login(user_gubin)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('tasks'))
        self.assertContains(response, _(TASK_NON_AUTHOR))
