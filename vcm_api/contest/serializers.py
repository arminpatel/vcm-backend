from rest_framework import serializers
from vcm_api.contest.models import Contest
from vcm_api.problem.serializers import ProblemSerializer


class RetrieveContestSerializer(serializers.ModelSerializer):

    problems = ProblemSerializer(many=True)

    class Meta:
        model = Contest
        fields = ['id', 'name', 'start_date_time', 'duration', 'problems']
