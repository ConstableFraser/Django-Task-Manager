from django.test import TestCase
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError

from task_manager.labels.models import Label


class LabelTestModelCase(TestCase):
    fixtures = ['Labels.json',
                'Users.json',
                'Statuses.json',
                'Tasks.json']

    def test_exist_labels(self):
        self.assertTrue(Label.objects.create(name="what_are_wonderful \
                                             world, o-o-ou!"))
        with self.assertRaises(IntegrityError):
            self.assertFalse(Label.objects.create(name="name_of_label"))

    def test_update_label(self):
        Label1 = Label.objects.get(id=1)
        Label1.name = "Name has been updated"
        Label1.save()
        Label1_new = Label.objects.get(name="Name has been updated")
        self.assertEqual(Label1_new.id, Label1.id)

    def test_delete_label(self):
        Label1 = Label.objects.get(id=1)
        Label7 = Label.objects.get(id=7)
        with self.assertRaises(ProtectedError):
            Label1.delete()
        Label7.delete()
        self.assertEqual(Label.objects.filter(id=1).count(), 1)
        self.assertEqual(Label.objects.filter(id=7).count(), 0)
