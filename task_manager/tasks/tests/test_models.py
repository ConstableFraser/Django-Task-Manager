from django.test import TestCase

from task_manager.tasks.models import Task
from task_manager.tasks.filter import TasksFilter


class TaskTestModelCase(TestCase):
    fixtures = ['Labels.json',
                'Users.json',
                'Statuses.json',
                'Tasks.json']

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
