from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=100,
                            null=False,
                            blank=False,
                            unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
