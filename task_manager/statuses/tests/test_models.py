from django.test import TestCase
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError

from task_manager.statuses.models import Status


class StatusTestModelCase(TestCase):
    fixtures = ['Labels.json',
                'Statuses.json',
                'Users.json',
                'Tasks.json']

    def test_exist_unique_status(self):
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
        default = Status.objects.get(id=115)
        with self.assertRaises(ProtectedError):
            self.assertFalse(completed.delete())
        self.assertTrue(default.delete())
        self.assertEqual(Status.objects.filter(id=111).count(), 1)
