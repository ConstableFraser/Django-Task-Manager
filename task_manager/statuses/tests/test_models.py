from django.test import TestCase
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError

from task_manager.statuses.models import Status


class StatusTestModelCase(TestCase):
    fixtures = ['Status_statuses.json',
                'Status_users.json',
                'Status_tasks.json']

    def test_exist_status(self):
        default = Status.objects.get(id=112)
        backlog = Status.objects.get(id=110)
        completed = Status.objects.get(id=111)
        self.assertEqual(f'{default}', 'default')
        self.assertEqual(f'{backlog}', 'backlog')
        self.assertEqual(f'{completed}', 'completed')
        self.assertTrue(Status.objects.create(name="what_the_status of \
                                             this process [temporary]"))
        with self.assertRaises(IntegrityError):
            self.assertFalse(Status.objects.create(name="default"))

    def test_update_status(self):
        backlog = Status.objects.get(id=110)
        backlog.name = 'Done'
        backlog.save()
        done = Status.objects.get(id=110)
        self.assertEqual(f'{done}', 'Done')

    def test_delete_status(self):
        completed = Status.objects.get(id=111)
        default = Status.objects.get(id=112)
        with self.assertRaises(ProtectedError):
            self.assertFalse(completed.delete())
        self.assertTrue(default.delete())
        self.assertEqual(Status.objects.filter(id=111).count(), 1)
