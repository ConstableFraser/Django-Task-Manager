from django.test import TestCase
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError

from task_manager.label.models import Label


class LabelTestModelCase(TestCase):
    fixtures = ['Label_labels.json',
                'Label_users.json',
                'Label_statuses.json',
                'Label_tasks.json']


    def test_create_label(self):
        Label1 = Label.objects.get(id=1)
        Label2 = Label.objects.get(id=2)
        Label3 = Label.objects.get(id=3)
        self.assertEqual(f'{Label1}', 'black_metka')
        self.assertEqual(f'{Label2}', 'f1')
        self.assertEqual(f'{Label3}', 'name_of_label')
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
        Label2 = Label.objects.get(id=2)
        with self.assertRaises(ProtectedError):
            Label1.delete()
        Label2.delete()
        self.assertEqual(Label.objects.filter(id=1).count(), 1)
        self.assertEqual(Label.objects.filter(id=2).count(), 0)