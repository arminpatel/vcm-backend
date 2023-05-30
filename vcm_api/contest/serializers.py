from django.contrib.auth import get_user_model
from rest_framework import serializers
from vcm_api.contest.models import Contest
from vcm_api.problem.serializers import ProblemSerializer
from vcm_api.problem.models import Problem


class ContestSerializer(serializers.ModelSerializer):

    problems = ProblemSerializer(many=True)

    class Meta:
        model = Contest
        fields = ['id', 'name', 'start_date_time',
                  'duration', 'problems']
        extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        User = get_user_model()
        current_user = User.objects.get(username=self.context.get("username"))
        problem_list = validated_data.pop('problems')

        contest = Contest.objects.create(**validated_data)
        contest.contest_creator.add(current_user)
        contest.participants.add(current_user)

        for problem in problem_list:
            problem_object = Problem.objects.create(**problem)
            contest.problems.add(problem_object)

        return contest
