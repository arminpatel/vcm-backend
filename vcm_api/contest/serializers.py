from rest_framework import serializers
from vcm_api.contest.models import Contest
from vcm_api.problem.serializers import ProblemSerializer
from vcm_api.problem.models import Problem
from django.core.exceptions import ValidationError
from datetime import datetime
import pytz


class ContestSerializer(serializers.ModelSerializer):

    problems = ProblemSerializer(many=True)

    class Meta:
        model = Contest
        fields = ['id', 'name', 'start_date_time',
                  'duration', 'problems']
        extra_kwargs = {'id': {'read_only': True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        current_time = datetime.now(pytz.UTC)
        start_date_time = instance.start_date_time
        if start_date_time > current_time:
            data['problems'].clear()
        return data

    def create(self, validated_data):
        current_user = self.context['request'].user
        problem_list = validated_data.pop('problems')

        contest = Contest.objects.create(**validated_data)
        contest.contest_creator.add(current_user)
        contest.participants.add(current_user)

        for problem in problem_list:
            try:
                problem_object = Problem.objects.create(**problem)
            except ValidationError as e:
                print(e)
                raise serializers.ValidationError(e)

            contest.problems.add(problem_object)

        return contest

    def update(self, instance, validated_data):
        updatable_fields = ['name', 'start_date_time', 'duration']

        for field in updatable_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        if "problems" in validated_data:
            problem_list = validated_data.pop('problems')
            current_problem = instance.problems.all()

            for problem in current_problem:
                if problem not in problem_list:
                    instance.problems.get(id=problem.id).delete()
                else:
                    problem_list.remove(problem)

            for problem in problem_list:
                problem_object = Problem.objects.create(**problem)
                instance.problems.add(problem_object)

        instance.save()
        return instance
