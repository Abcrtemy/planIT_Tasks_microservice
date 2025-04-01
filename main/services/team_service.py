from main.serializers import TeamSerializer
from main.models import Team

class TeamService:
    @staticmethod
    def create(data):
        data["team_leader"] = data["creator_id"]
        serializer = TeamSerializer(data = data)
        if serializer.is_valid():
            return serializer.save()
        raise Exception(f"serializer error{serializer.errors}")
    @staticmethod
    def update(data, teamID, creator_id):
        team = Team.objects.get(id=teamID, creator_id = creator_id)
        serializer = TeamSerializer(team, data=data, partial = True)
        if serializer.is_valid():
            return serializer.save()
        raise Exception(f"serializer error{serializer.errors}")
    @staticmethod
    def delete(teamID, creator_id):
        team = Team.objects.get(id=teamID, creator_id = creator_id)
        team.delete()