from django.test import TestCase
from django.db import IntegrityError

from task_manager.task.models import (Task, User, Status)
from task_manager.task.filter import TasksFilter


class TaskTestModelCase(TestCase):
    fixtures = ['Task_labels.json',
                'Task_users.json',
                'Task_statuses.json',
                'Task_tasks.json']

    def test_filter_task(self):
        qs = Task.objects.all()
        f = TasksFilter(data={'status': '',
                              'executor': '',
                              'author': '',
                              'labels': '',
                              'self_tasks': False},
                        queryset=qs)
        self.assertEqual(f.qs.count(), qs.count())
        f = TasksFilter(data={'status': 110,
                              'executor': 150,
                              'author': '',
                              'labels': '',
                              'self_tasks': False},
                        queryset=qs)
        self.assertEqual(f.qs.count(), 1)
        f = TasksFilter(data={'status': 111,
                              'executor': 152,
                              'author': '',
                              'labels': '',
                              'self_tasks': False},
                        queryset=qs)
        self.assertEqual(f.qs.count(), 1)
