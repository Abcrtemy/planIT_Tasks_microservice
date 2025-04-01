from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import requests

from functools import wraps

from main.models import Task, Project, Team
from .serializers import TaskSerializer, ProjectSerializer, TeamSerializer
from .services.minIO_service import FileHandler
from .services.mongo_service import TaskHistory
from .services.project_service import ProjectService
from .services.team_service import TeamService
from .permissions import require_auth_creator, require_auth_user, tokenGetUser

import json


class TasksGetView(APIView):
    def get(self, request):
        if request.method == 'GET':
            user_id = tokenGetUser(request.headers.get('Authorization'))
            if (not user_id):
                return Response({"error": "Missing or invalid token"}, status=403)
            tasks = Task.objects.filter(user_id = user_id)

            if tasks.exists():
                serializer = TaskSerializer(tasks, many = True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No tasks found for this user."}, status=status.HTTP_404_NOT_FOUND)

class TaskView(APIView):
    @require_auth_user
    def post(self, request):
        if "file" in request.data:
            file = request.FILES.get("file")
            fileHandler = FileHandler(file.name)
            filePath = fileHandler.uploadFile(file)
            request.data['file'] = filePath

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()

            taskHistory = TaskHistory(task.id, request.data.get('user_id'))
            taskHistory.create()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @require_auth_user
    def delete(self, request, taskId):
        user_id = tokenGetUser(request.headers.get('Authorization'))
        try:
            task = Task.objects.get(id=taskId, user_id = user_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        if task.file:
            fileHandler = FileHandler(task.file)
            fileHandler.deleteFile()
        taskHistory = TaskHistory(task.id, user_id)
        taskHistory.delete()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    @require_auth_user
    def patch(self, request, taskId):
        try:
            task = Task.objects.get(id=taskId, user_id = request.data.get('user_id'))
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            taskHistory = TaskHistory(task.id, request.data.get('user_id'))
            taskHistory.update()

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class ProjectView(APIView):
    @require_auth_creator
    def post(self, request):
        try:
            project = ProjectService.create(request.data)
            return Response(ProjectSerializer(project).data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(f"error: {e}", status=status.HTTP_400_BAD_REQUEST)
    
    @require_auth_creator
    def patch(self, request, projectID):
        try:
            project = ProjectService.update(data = request.data, projectID = projectID, creator_id = request.data.get('creator_id'))
            return Response(ProjectSerializer(project).data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(f"error: {e}", status=status.HTTP_400_BAD_REQUEST)
        
    @require_auth_creator
    def delete(self, request, projectID):
        creator_id = tokenGetUser(request.headers.get('Authorization'))
        try:
            ProjectService.delete(projectID = projectID, creator_id = creator_id)
            return Response("sucsess", status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(f"error: {e}", status=status.HTTP_400_BAD_REQUEST)


class TeamView(APIView):
    @require_auth_creator
    def post(self, request):
        try:
            team = TeamService.create(request.data)
            return Response(TeamSerializer(team).data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(f"error: {e}", status=status.HTTP_400_BAD_REQUEST)
    
    @require_auth_creator
    def patch(self, request, teamID):
        try:
            team = TeamService.update(data = request.data, teamID = teamID, creator_id = request.data.get('creator_id'))
            return Response(TeamSerializer(team).data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(f"error: {e}", status=status.HTTP_400_BAD_REQUEST)
        
    @require_auth_creator
    def delete(self, request, teamID):
        creator_id = tokenGetUser(request.headers.get('Authorization'))
        try:
            TeamService.delete(teamID = teamID, creator_id = creator_id)
            return Response("sucsess", status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(f"error: {e}", status=status.HTTP_400_BAD_REQUEST)
