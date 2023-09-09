from django.db import models

from ..status.models import Status
from ..user.models import User
from ..label.models import Label


class Task(models.Model):
    name = models.CharField(max_length=150,
                            null=False,
                            blank=False,
                            unique=True
                            )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(Status,
                               on_delete=models.PROTECT,
                               null=False
                               )
    author = models.ForeignKey(User,
                               on_delete=models.PROTECT,
                               null=False,
                               related_name='taskTOauthor')
    executor = models.ForeignKey(User,
                                 on_delete=models.PROTECT,
                                 null=True,
                                 related_name='taskTOdoer')
    labels = models.ManyToManyField(Label,
                                    through='TaskToLabel',
                                    through_fields=('task', 'label'))

    def __str__(self):
        return self.name


class TaskToLabel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
