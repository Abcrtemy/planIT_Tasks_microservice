from main.serializers import ProjectSerializer
from main.models import Project

class ProjectService:
    @staticmethod
    def create(data):
        serializer = ProjectSerializer(data = data)
        if serializer.is_valid():
            return serializer.save()
        raise Exception(f"serializer error{serializer.errors}")
    @staticmethod
    def update(data, projectID, creator_id):
        project = Project.objects.get(id=projectID, creator_id = creator_id)
        serializer = ProjectSerializer(project, data=data, partial = True)
        if serializer.is_valid():
            return serializer.save()
        raise Exception(f"serializer error{serializer.errors}")
    @staticmethod
    def delete(projectID, creator_id):
        project = Project.objects.get(id=projectID, creator_id = creator_id)
        project.delete()