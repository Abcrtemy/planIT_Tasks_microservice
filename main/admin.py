from django.contrib import admin
from .models import Task, Project, Project_user, Sprint, Company, Company_user
# Register your models here.
admin.site.register(Task)
admin.site.register(Project)
admin.site.register(Sprint)
admin.site.register(Company)
# admin.site.register(Team)
admin.site.register(Project_user)
admin.site.register(Company_user)
# admin.site.register(Team)
