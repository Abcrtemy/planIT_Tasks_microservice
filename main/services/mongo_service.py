from pymongo import MongoClient
from datetime import datetime

class TaskHistory():
    def __init__(self, task_id, user_id):
        client = MongoClient("mongodb://mongo:27017")  
        db = client['task_meta_db']  
        self.collection = db['task_meta']
        now = datetime.now().isoformat()
        self.task_id = task_id
        self.data = {
            "task_id": task_id,
            "action_type": "",
            "time": now,
            "user_id": user_id,
        }
    def create (self):
        try:
            self.data['action_type'] = "create"
            self.collection.insert_one(self.data)
        except Exception as e:
            raise Exception(f"Mongo exeption: {str(e)}")
    def delete (self):
        try:
            self.data['action_type'] = "delete"
            self.collection.insert_one(self.data)
        except Exception as e:
            raise Exception(f"Mongo exeption: {str(e)}")
    def update (self):
        try:
            self.data['action_type'] = "update"
            self.collection.insert_one(self.data)
        except Exception as e:
            raise Exception(f"Mongo exeption: {str(e)}")
    def get_all_history(self):
        return self.collection.find({"task_id": self.task_id})