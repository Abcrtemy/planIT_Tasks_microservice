from main.models import Sprint, Project
class SprintService:
    @staticmethod
    def create(projectID):
        try:
            project = Project.objects.get(id=projectID)
        except Project.DoesNotExist:
            raise ValueError("Project not found")
        
        number = SprintService.calc_number(projectID)

        Sprint.objects.filter(project=project, is_active=True).update(is_active=False)

        sprint = Sprint.objects.create(
            project=project,
            number=number,
            is_active=True
        )
        return sprint
    @staticmethod
    def delete_all(projectID):
        deleted_count, _ = Sprint.objects.filter(project_id=projectID).delete()
        return deleted_count
    @staticmethod
    def calc_number(projectID):
        last_sprint = Sprint.objects.filter(project_id=projectID).order_by("-number").first()
        return (last_sprint.number + 1) if last_sprint else 1
    @staticmethod
    def get_active_sprint(projectID):
        return Sprint.objects.filter(project_id=projectID, is_active=True).first()
    @staticmethod
    def complete_sprint(projectID):
        active_sprint = SprintService.get_active_sprint(projectID)
        if active_sprint:
            active_sprint.is_active = False
            active_sprint.save()
        return SprintService.create(projectID)