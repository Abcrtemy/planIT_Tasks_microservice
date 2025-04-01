from rest_framework import serializers
from .models import Task, Project, Team


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ['creationTime']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ['created_at']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        exclude = ['created_at']