from django.test import TestCase

from task_manager.status.models import Status


class StatusTestModelCase(TestCase):
    fixtures = ['statuses.json']


    def test_create_status(self):
        default = Status.objects.get(name='default')
        backlog = Status.objects.get(name='backlog')
        completed = Status.objects.get(name='completed')
        self.assertEqual(f'{default}', 'default')
        self.assertEqual(f'{backlog}', 'backlog')
        self.assertEqual(f'{completed}', 'completed')


    def test_update_status(self):
        completed = Status.objects.get(name='completed')
        completed.name = 'Done'
        completed.save()
        done = Status.objects.get(name='Done')
        self.assertEqual(f'{done}', 'Done')


    def test_delete_status(self):
        count_before = Status.objects.only('id').count()
        completed = Status.objects.get(name='completed')
        default = Status.objects.get(name='default')
        completed.delete()
        default.delete()
        self.assertEqual(Status.objects.filter(name='completed').count(), 0)
        self.assertEqual(Status.objects.filter(name='default').count(), 0)
