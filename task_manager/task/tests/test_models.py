from django.test import TestCase

from task_manager.task.models import Task


class TaskTestModelCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json']


    def test_create_tasks(self):
        Task1 = Task.objects.get(id=1)
        Task2 = Task.objects.get(id=2)
        Task3 = Task.objects.get(id=3)
        self.assertEqual(f'{Task1}', 'Nothing to do')
        self.assertEqual(f'{Task2}', 'complete a professional course')
        self.assertEqual(f'{Task3}', 'do the something')


    def test_update_Task(self):
        Task1 = Task.objects.get(id=1)
        Task1.executor = None
        Task1.name = "What's happened"
        Task1.description = ''
        Task1.save()
        Task1_new = Task.objects.get(name="What's happened")
        self.assertEqual(Task1_new.id, Task1.id)


    def test_delete_Task(self):
        Task2 = Task.objects.get(id=2)
        Task3 = Task.objects.get(id=3)
        Task2.delete()
        Task3.delete()
        self.assertEqual(Task.objects.filter(id=2).count(), 0)
        self.assertEqual(Task.objects.filter(id=3).count(), 0) 