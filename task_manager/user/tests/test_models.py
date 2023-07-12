from django.test import TestCase

from task_manager.user.models import User


class UserTestModelCase(TestCase):
    fixtures = ['users.json']


    def test_create_user(self):
        Gates = User.objects.get(first_name='Bill', last_name='Gates')
        Jobs = User.objects.get(first_name='Steve', last_name='Jobs')
        Gubin = User.objects.get(first_name='Andrei', last_name='Gubin')
        self.assertEqual(f'{Gates}', 'Bill Gates')
        self.assertEqual(f'{Jobs}', 'Steve Jobs')
        self.assertEqual(f'{Gubin}', 'Andrei Gubin')


    def test_update_user(self):
        Gubin = User.objects.get(first_name='Andrei', last_name='Gubin')
        Gubin.first_name = 'Rick'
        Gubin.last_name = 'Astley'
        Gubin.username = 'RAstley'
        Gubin.save()
        Astley = User.objects.get(username='RAstley')
        self.assertEqual(f'{Astley}', 'Rick Astley')


    def test_delete_user(self):
        count_before = User.objects.only('id').count()
        Gates = User.objects.get(first_name='Bill', last_name='Gates')
        Jobs = User.objects.get(first_name='Steve', last_name='Jobs')
        Gates.delete()
        Jobs.delete()
        count_after = User.objects.only('id').count()
        self.assertEqual(count_after, count_before-2)
