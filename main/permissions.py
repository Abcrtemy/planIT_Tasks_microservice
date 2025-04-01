from rest_framework.response import Response
import requests
from functools import wraps



def tokenGetUser(token):
    if not token or not token.startswith('Bearer '):
        return None 
    token = token.split(' ')[1]
    response = requests.post("http://autenticate-app:8001/auth/validate/", json={"token": token})
    if response.status_code != 200:
        return None
    user_data= response.json()
    return user_data.get("user_id")


def require_auth_creator(view_func):
    @wraps(view_func)
    def wrapped_view(self, request, *args, **kwargs):
        user_id = tokenGetUser(request.headers.get('Authorization'))
        if not user_id:
            return Response({"error": "Missing or invalid token"}, status=403)
        request.data["creator_id"] = user_id

        return view_func(self, request, *args, **kwargs)
    return wrapped_view

def require_auth_user(view_func):
    @wraps(view_func)
    def wrapped_view(self, request, *args, **kwargs):
        user_id = tokenGetUser(request.headers.get('Authorization'))
        if not user_id:
            return Response({"error": "Missing or invalid token"}, status=403)
        if request.data:
            request.data["user_id"] = user_id

        return view_func(self, request, *args, **kwargs)
    return wrapped_view