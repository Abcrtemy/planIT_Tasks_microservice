from main.serializers import ProjectSerializer
from main.models import Project, Project_user, Company_user, Company
from main.services.sprint_service import SprintService


class ProjectService:

    @staticmethod
    def create(data):
        # print(data)
        data['team_leader'] = data['creator_id']
        serializer = ProjectSerializer(data = data)
        if serializer.is_valid():
            project = serializer.save()
            SprintService.create(project.id)
            Project_user.objects.create(project = project, user_id = data['creator_id'])
            ProjectService.calculate_users(project.id)
            return ProjectSerializer(project).data
        raise Exception(f"serializer error{serializer.errors}")
    @staticmethod

    def update(data, projectID, creator_id):
        print(data)
        project = Project.objects.get(id=projectID, creator_id = creator_id)
        serializer = ProjectSerializer(project, data=data, partial = True) 
        if serializer.is_valid():
            serializer.update(project,  data)
            return ProjectSerializer(serializer.update(project,  data)).data
        raise Exception(f"serializer error{serializer.errors}")
    
    @staticmethod
    def delete_user(user_id, team_id):
        project = Project.objects.get(id=team_id)
        project_user = Project_user.objects.get(project = project, user_id = user_id)
        project_user.delete()
        ProjectService.calculate_users(project.id)

    @staticmethod
    def add_user(user_id, team_id):
        project = Project.objects.get(id=team_id)
        Project_user.objects.create(project = project, user_id = user_id)
        ProjectService.calculate_users(project.id)

    @staticmethod
    def get_all_by_user_id(user_id):
        company_ids = Company_user.objects.filter(user_id=user_id).values_list('company_id', flat=True)
        companies = Company.objects.filter(id__in=company_ids)
        user_project_ids = Project_user.objects.filter(user_id=user_id).values_list('project', flat=True)
        response_data = []
        for company in companies:
            all_projects = Project.objects.filter(company=company)
            joined_projects = all_projects.filter(id__in=user_project_ids)
            available_projects = all_projects.exclude(id__in=user_project_ids)
            response_data.append({
                'company_id': company.id,
                'company_name': company.name,
                'joined_projects': ProjectSerializer(joined_projects, many=True).data,
                'available_projects': ProjectSerializer(available_projects, many=True).data,
            })
        return response_data
    
    @staticmethod
    def calculate_users(project_id):
        project = Project.objects.get(id=project_id)
        user_project = Project_user.objects.filter(project=project).distinct()
        project.amount_of_persons = len(user_project)
        project.save()

    @staticmethod
    def delete(projectID, creator_id):
        project = Project.objects.get(id=projectID, creator_id = creator_id)
        Project_user.objects.filter(project=project).delete()
        SprintService.delete_all(project.id)
        # project_user.delete()
        project.delete()