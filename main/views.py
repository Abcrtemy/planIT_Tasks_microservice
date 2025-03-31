from django.shortcuts import render
from rest_framework.views import APIView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import requests
import boto3
from botocore.exceptions import ClientError
from django.conf import settings

import os
# import redis
import pymongo
from pymongo import MongoClient

from minio import Minio
from minio.error import S3Error

from datetime import datetime

from main.models import Task
from .serializers import TaskSerializer

import json


# redis_client = redis.Redis(host='redis', port=6379, db=0)


# minIOclient = Minio(
#     "localhost:9000",  # Адрес MinIO
#     access_key="admin",  # Ключ доступа
#     secret_key="secretpassword",  # Секретный ключ
#     secure=False,  # Используем HTTP, если по HTTPS - установи True
# )
# bucket_name = "task-bucket"
# if not minIOclient.bucket_exists(bucket_name):
#     minIOclient.make_bucket(bucket_name)


INPUT_DIR = os.path.expanduser("~/Desktop/input")

client = MongoClient("mongodb://mongo:27017")  # mongo - имя контейнера, 27017 - порт по умолчанию
db = client['task_meta_db']  # Название базы данных
collection = db['task_meta']

def tokenGetUser(token):
    if not token or not token.startswith('Bearer '):
        return None 
    token = token.split(' ')[1]
    response = requests.post("http://autenticate-app:8001/auth/validate/", json={"token": token})
    if response.status_code != 200:
        return None
    user_data= response.json()
    return user_data.get("user_id")

# def get_task_metadata(task_id):
#     meta_key = f"task_meta_{task_id}"
#     meta_info = redis_client.hgetall(meta_key)
#     return {k.decode('utf-8'): v.decode('utf-8') for k, v in meta_info.items()}


class FileHandler():
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.MINIO_ENDPOINT,
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME

    def file_exists(self, file_key):
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=file_key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                return False
            raise
    
    def generate_unique_filename(self, file_key):
        base_key, ext = os.path.splitext(file_key)
        counter = 1
        print (base_key, ext)
        new_file_key = file_key
        while self.file_exists(f"{new_file_key}"):
            new_file_key = f"{base_key}_{counter}{ext}"
            counter += 1
        return new_file_key

    def extract_file_key(self, file_url):
        if not file_url.startswith(settings.MINIO_ENDPOINT):
            raise ValueError("Некорректный URL файла")

        file_key = file_url.replace(f"{settings.MINIO_ENDPOINT}/{self.bucket_name}/", "")
        return file_key

    
    def deleteFile(self, file_path):
        file_key = self.extract_file_key(file_path)
        print(file_key)
        if self.file_exists(file_key):
            try:
                self.s3_client.delete_object(Bucket=self.bucket_name, Key=f"{file_key}")
                return True
            except Exception as e:
                # raise Exception(f"Ошибка при удалении файла: {str(e)}")
                return False
       
            
    def uploadFile(self, file):
        self.file_key = f"tasks/{file.name}"
        self.file = file 
        if self.file_exists(self.file_key):
            self.file_key = self.generate_unique_filename(self.file_key)
        self.s3_client.upload_fileobj(self.file, settings.MINIO_BUCKET_NAME, self.file_key)
        file_url = f"{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET_NAME}/{self.file_key}"
        return file_url

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
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request):
        if request.method == 'POST':
            user_id = tokenGetUser(request.headers.get('Authorization'))
            if (not user_id):
                return Response({"error": "Missing or invalid token"}, status=403)
            
            request_data = request.data.copy()  
            request_data['user_id'] = user_id

            if "file" in request.FILES:
                fileHandler = FileHandler()
                filePath = fileHandler.uploadFile(request.FILES.get("file"))
                request_data['file'] = filePath

            serializer = TaskSerializer(data=request_data)
            if serializer.is_valid():
                task = serializer.save()
                now = datetime.now().isoformat()
                data = {
                    "task_id": task.id,
                    "change_type": "create",
                    "timestamp": now,
                    "comment": "New task created"
                }
                collection.insert_one(data)

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
            fileHandler = FileHandler()
            fileHandler.deleteFile(task.file)
        task.delete()
        now = datetime.now().isoformat()
        data = {
            "task_id": task.id,
            "change_type": "delete",
            "timestamp": now,
            "comment": "Task deleted"
        }
        collection.insert_one(data)
        # meta_key = f"task_meta_{taskId}"
        # redis_client.delete(meta_key)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    def patch(self, request, taskId):
        user_id = tokenGetUser(request.headers.get('Authorization'))
        if (not user_id):
            return Response({"error": "Missing or invalid token"}, status=403)
        task_data = collection.find({"task_id": taskId, "change_type": "patch"})
        for task_ in task_data:
            print(task_)
        # print('test')
        task_data = collection.find({"task_id": taskId})
        for task_ in task_data:
            print(task_)
        try:
            task = Task.objects.get(id=taskId, user_id = user_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            now = datetime.now().isoformat()
            data = {
                "task_id": task.id,
                "change_type": "patch",
                "timestamp": now,
                "comment": "Task updated"
            }
            collection.insert_one(data)
            # meta_key = f"task_meta_{taskId}"
            # redis_client.hset(meta_key, "last_modified", datetime.now().isoformat())

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
