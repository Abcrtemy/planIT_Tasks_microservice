import boto3
from django.conf import settings
from botocore.exceptions import ClientError
import os

class FileHandler():
    def __init__(self, file_url):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.MINIO_ENDPOINT,
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self.file_key = self.extract_file_key(file_url)

    def file_exists(self):
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=self.file_key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                return False
            raise
    
    def generate_unique_filename(self):
        base_key, ext = os.path.splitext(self.file_key)
        counter = 1
        while self.file_exists():
            self.file_key = f"{base_key}_{counter}{ext}"
            counter += 1

    def extract_file_key(self, file_url):
        if not file_url.startswith(f"{settings.MINIO_ENDPOINT}/{self.bucket_name}/"):
            return f"tasks/{file_url}"

        file_key = file_url.replace(f"{settings.MINIO_ENDPOINT}/{self.bucket_name}/", "")
        return file_key

    def deleteFile(self):
        file_key = self.file_key
        if self.file_exists():
            try:
                self.s3_client.delete_object(Bucket=self.bucket_name, Key=f"{file_key}")
                return True
            except Exception as e:
                return False

    def uploadFile(self, file):
        self.file = file 
        if self.file_exists():
            self.generate_unique_filename()
        self.s3_client.upload_fileobj(self.file, settings.MINIO_BUCKET_NAME, self.file_key)
        file_url = f"{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET_NAME}/{self.file_key}"
        return file_url