from django.db import models

from ..status.models import Status
from ..user.models import User


class Task(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(Status,
                               on_delete=models.PROTECT,
                               null=False)
    author = models.ForeignKey(User,
                               on_delete=models.PROTECT,
                               null=False,
                               related_name='taskTOauthor')
    executor = models.ForeignKey(User,
                                 on_delete=models.PROTECT,
                                 null=True,
                                 related_name='taskTOdoer')

    def __str__(self):
        return self.name
