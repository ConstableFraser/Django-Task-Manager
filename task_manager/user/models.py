from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password1']

    def __str__(self):
        return self.first_name + " " + self.last_name
