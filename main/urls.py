from django.contrib import admin
from django.urls import path
from .views import TaskView, TasksGetView, ProjectView
from main import views


app_name = 'main'

urlpatterns = [
    path('', TasksGetView.as_view(), name='taskBoard'),
    path('task/create/', TaskView.as_view(), name='taskCreate'),
    path('task/<int:taskId>/', TaskView.as_view(), name='taskDelete'),
    path('task/<int:taskId>/', TaskView.as_view(), name='taskUpdate'),
    # path('task/update/', views.taskUpdate, name='taskUpdate'),

    # path('project/save/', ProjectView.as_view({'post': 'save'}), name='save_project'),
    path('project/create/', ProjectView.as_view({'post': 'post'}), name='create_project'),
    path('project/<int:projectID>/', ProjectView.as_view({'patch': 'patch'}), name='projectUpdate'),
    path('project/<int:projectID>/', ProjectView.as_view({'delete': 'delete'}), name='projectDelete'),
    path('project/get/', ProjectView.as_view({'get': 'get'}), name='teamGet'),
    path('project/<int:project_id>/add_user', ProjectView.as_view({'post': 'add_user'}), name='add_user'),
    path('project/<int:project_id>/delete_user', ProjectView.as_view({'post': 'delete_user'}), name='delete_user'),

    # path('team/create/', TeamView.as_view({'post': 'post'}), name='teamCreate'),
    # path('team/<int:teamID>/', TeamView.as_view({'patch': 'patch'}), name='teamUpdate'),
    # path('team/get/', TeamView.as_view({'get': 'get'}), name='teamGet'),
    # path('team/<int:teamID>/add_user', TeamView.as_view({'post': 'add_user'}), name='add_user'),
    # path('team/create/', TaskView.as_view(), name='teamCreate'),

]