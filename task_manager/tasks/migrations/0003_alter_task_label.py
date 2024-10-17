# Generated by Django 5.1.1 on 2024-10-17 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0002_remove_task_label_task_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='label',
            field=models.ManyToManyField(related_name='tasks', to='labels.label'),
        ),
    ]