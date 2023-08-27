from django.test import TestCase
from django.db import IntegrityError

from task_manager.task.models import (Task, User, Status)
from task_manager.task.filter import TasksFilter
from task_manager.user.models import User


class TaskTestModelCase(TestCase):
    fixtures = ['Task_labels.json',
                'Task_users.json',
                'Task_statuses.json',
                'Task_tasks.json']

    def test_create_tasks(self):
        Task1 = Task.objects.get(id=1)
        Task2 = Task.objects.get(id=2)
        Task3 = Task.objects.get(id=3)
        self.assertEqual(f'{Task1}', 'Nothing to do')
        self.assertEqual(f'{Task2}', 'complete a professional course')
        self.assertEqual(f'{Task3}', 'do the something')
        stts = Status.objects.get(id=110)
        usr = User.objects.get(id=151)
        self.assertTrue(Task.objects.create(status=stts,
                                            author=usr,
                                            name="do what is right and \
                                            come what may..."))
        with self.assertRaises(IntegrityError):
            self.assertFalse(Task.objects.create(status=stts,
                                                 author=usr,
                                                 name="Nothing to do"))

    def test_update_task(self):
        Task1 = Task.objects.get(id=1)
        Task1.executor = None
        Task1.name = "What's happened"
        Task1.description = ''
        Task1.save()
        Task1_new = Task.objects.get(name="What's happened")
        self.assertEqual(Task1_new.id, Task1.id)

    def test_delete_task(self):
        Task2 = Task.objects.get(id=2)
        Task3 = Task.objects.get(id=3)
        Task2.delete()
        Task3.delete()
        self.assertEqual(Task.objects.filter(id=2).count(), 0)
        self.assertEqual(Task.objects.filter(id=3).count(), 0)

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
