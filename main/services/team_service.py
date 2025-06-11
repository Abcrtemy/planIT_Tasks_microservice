# from main.serializers import TeamSerializer
# from main.models import Team, Team_user

# class TeamService:
#     @staticmethod
#     def create(data):
#         data["team_leader"] = data["creator_id"]
#         serializer = TeamSerializer(data = data)
#         if serializer.is_valid():
#             return TeamSerializer(serializer.save()).data
#         raise Exception(f"serializer error{serializer.errors}")
#     @staticmethod
#     def update(data, teamID, creator_id):
#         team = Team.objects.get(id=teamID, creator_id = creator_id)
#         serializer = TeamSerializer(team, data=data, partial = True)
#         if serializer.is_valid():
#             return TeamSerializer(serializer.save()).data
#         raise Exception(f"serializer error{serializer.errors}")
#     @staticmethod
#     def add_user(user_id, team_id):
#         team = Team.objects.get(id=team_id)
#         Team_user.objects.create(team = team, user_id = user_id)

#     @staticmethod
#     def get_all_by_user_id(user_id):
#         # print("hello")
#         teams = Team.objects.filter(members__user_id=user_id).distinct() 
#         print("ad")
#         serializer = TeamSerializer(teams, many = True)
#         print(serializer.data)
#         return serializer.data



#     @staticmethod
#     def delete(teamID, creator_id):
#         team = Team.objects.get(id=teamID, creator_id = creator_id)
#         team.delete()