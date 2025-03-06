from django.shortcuts import render
from rest_framework.views import APIView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

from main.models import Task
from .serializers import TaskSerializer

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

            serializer = TaskSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
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
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
