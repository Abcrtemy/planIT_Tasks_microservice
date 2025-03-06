from django.contrib import admin
from django.urls import path
from .views import TaskView, TasksGetView
from main import views


app_name = 'main'

urlpatterns = [
    path('', TasksGetView.as_view(), name='taskBoard'),
    path('task/create/', TaskView.as_view(), name='taskCreate'),
    path('task/<int:taskId>/', TaskView.as_view(), name='taskDelete'),
    path('task/<int:taskId>/', TaskView.as_view(), name='taskUpdate'),
    # path('task/update/', views.taskUpdate, name='taskUpdate'),

]