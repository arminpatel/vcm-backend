from rest_framework import serializers
from vcm_api.problem.models import Problem
from vcm_api.submission.models import Submission


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'name', 'link', 'score', 'online_judge', 'is_solved']

    is_solved = serializers.SerializerMethodField()

    def get_is_solved(self, instance):
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            return False
        firstsub = Submission.objects.filter(user=current_user, problem=instance).first()
        if firstsub is None:
            return False
        return firstsub.correct_answer
