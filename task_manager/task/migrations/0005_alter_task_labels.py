# Generated by Django 4.2.2 on 2023-08-07 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0002_label_created_at'),
        ('task', '0004_tasktolabel_task_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(null=True, through='task.TaskToLabel', to='label.label'),
        ),
    ]