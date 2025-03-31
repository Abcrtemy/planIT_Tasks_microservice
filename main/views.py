from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import requests

from main.models import Task
from .serializers import TaskSerializer
from .services.minIO_service import FileHandler
from .services.mongo_service import TaskHistory

import json

def tokenGetUser(token):
    if not token or not token.startswith('Bearer '):
        return None 
    token = token.split(' ')[1]
    response = requests.post("http://autenticate-app:8001/auth/validate/", json={"token": token})
    if response.status_code != 200:
        return None
    user_data= response.json()
    return user_data.get("user_id")

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
    def post(self, request):
        if request.method == 'POST':

            user_id = tokenGetUser(request.headers.get('Authorization'))
            if (not user_id):
                return Response({"error": "Missing or invalid token"}, status=403)
            
            request_data = request.data.copy()  
            request_data['user_id'] = user_id

            if "file" in request.data:
                file = request.FILES.get("file")
                fileHandler = FileHandler(file.name)
                filePath = fileHandler.uploadFile(file)
                request_data['file'] = filePath

            serializer = TaskSerializer(data=request_data)
            if serializer.is_valid():
                task = serializer.save()

                taskHistory = TaskHistory(task.id, user_id)
                taskHistory.create()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, taskId):
        user_id = tokenGetUser(request.headers.get('Authorization'))
        if (not user_id):
            return Response({"error": "Missing or invalid token"}, status=403)
        
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

    def patch(self, request, taskId):
        user_id = tokenGetUser(request.headers.get('Authorization'))
        if (not user_id):
            return Response({"error": "Missing or invalid token"}, status=403)
        try:
            task = Task.objects.get(id=taskId, user_id = user_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            taskHistory = TaskHistory(task.id, user_id)
            taskHistory.update()

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
