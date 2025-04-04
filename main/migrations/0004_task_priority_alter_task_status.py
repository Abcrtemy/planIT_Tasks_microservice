# Generated by Django 5.1.5 on 2025-02-18 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_user_task_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low', max_length=20, verbose_name='Приоритет'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('backLog', 'Backlog'), ('toDo', 'Todo'), ('inProgressLog', 'Inprogress'), ('done', 'Done')], default='toDo', max_length=20, verbose_name='Статус'),
        ),
    ]
