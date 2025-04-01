from django.contrib import admin
from django.urls import path
from .views import TaskView, TasksGetView, ProjectView, TeamView
from main import views


app_name = 'main'

urlpatterns = [
    path('', TasksGetView.as_view(), name='taskBoard'),
    path('task/create/', TaskView.as_view(), name='taskCreate'),
    path('task/<int:taskId>/', TaskView.as_view(), name='taskDelete'),
    path('task/<int:taskId>/', TaskView.as_view(), name='taskUpdate'),
    # path('task/update/', views.taskUpdate, name='taskUpdate'),

    path('project/create/', ProjectView.as_view(), name='projectCreate'),
    path('project/<int:projectID>/', ProjectView.as_view(), name='projectUpdate'),

    path('team/create/', TeamView.as_view(), name='teamCreate'),
    path('team/<int:teamID>/', TeamView.as_view(), name='teamUpdate'),
    # path('team/create/', TaskView.as_view(), name='teamCreate'),

]