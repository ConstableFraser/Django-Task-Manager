# Generated by Django 4.2.4 on 2023-09-10 10:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tasks', '0001_initial'),
        ('statuses', '0001_initial'),
        ('labels', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='taskTOauthor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='taskTOdoer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(through='tasks.TaskToLabel', to='labels.label'),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='statuses.status'),
        ),
    ]
