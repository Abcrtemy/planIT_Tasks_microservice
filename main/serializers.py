from rest_framework import serializers
from .models import Task, Project, Sprint, Company


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ['creationTime']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
    def update(self, instance, validated_data):
        print("update")
        for attr, value in validated_data.items():
            if attr == 'company' and isinstance(value, int):
                value = Company.objects.get(id=value)
            setattr(instance, attr, value)
        instance.save()
        return instance

class SprintSrializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        exclude = ['end_time']

# class TeamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Team
#         fields = '__all__'