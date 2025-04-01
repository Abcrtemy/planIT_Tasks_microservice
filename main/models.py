from django.db import models
from datetime import timedelta

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

    file = models.CharField(max_length=200, null=True, blank=True)


class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator_id = models.IntegerField()

    def __str__(self) -> str:
        return self.name

class Sprint(models.Model):
    is_active = models.BooleanField(default=True)
    start_time = models.DateTimeField(auto_now_add=True)
    number = models.IntegerField()
    duration = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="sprints")
    
    @property
    def end_time(self):
        return self.start_time + timedelta(days=self.duration)
    
    def __str__(self) -> str:
        return self.number

class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    amount_of_persons = models.IntegerField(default=0)
    project = models.ManyToManyField(Project, blank = True, related_name='team')
    team_leader = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator_id = models.IntegerField()

    def __str__(self) -> str:
        return self.name