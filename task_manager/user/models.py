from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(_("First name"),
                                  max_length=150,
                                  blank=False)
    last_name = models.CharField(_("Last name"),
                                 max_length=150,
                                 blank=False)

    REQUIRED_FIELDS = [first_name, last_name]

    def __str__(self):
        return self.first_name + " " + self.last_name
