from django.db import models

# Create your models here.
class Task (models.Model):
    class PriorityChoices(models.TextChoices):
        low = 'low'
        medium = 'medium'
        high = 'high'

    class StatusChoices(models.TextChoices):
        backLog = 'backLog'
        inProgress = 'inProgress'
        propose = 'propose'
        done = 'done'

    class TypeChoices(models.TextChoices):
        bug = 'bug'
        feature = 'feature'

    name = models.CharField(max_length=200, unique=True, verbose_name='Название')
    description = models.CharField(max_length=2000,null=True, blank=True, verbose_name='Описание')
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.backLog, verbose_name='Статус')
    tType = models.CharField(max_length=20, choices=TypeChoices.choices, default=TypeChoices.bug, verbose_name='Тип')
    # sprint = models.IntegerField(null=True, blank=True, verbose_name='Спринт')
    creationTime = models.DateTimeField(auto_now=False, auto_now_add=True)
    estimatedDuration = models.IntegerField(default = 1, verbose_name='Оценочное время')

    priority = models.CharField(max_length=20, choices=PriorityChoices.choices, default=PriorityChoices.low, verbose_name='Приоритет')

    user_id = models.IntegerField(null=True, blank=True, verbose_name='Пользователь')
