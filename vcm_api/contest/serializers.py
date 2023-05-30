from rest_framework import serializers
from vcm_api.contest.models import Contest
from vcm_api.problem.serializers import ProblemSerializer


class RetrieveContestSerializer(serializers.ModelSerializer):

    problems = ProblemSerializer(many=True)
    contest_creator = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault)

    class Meta:
        model = Contest
        fields = ['id', 'name', 'start_date_time',
                  'duration', 'problems', 'contest_creator']
        extra_kwargs = {'id': {'read_only': True},
                        'contest_creator': {'write_only': True}}
