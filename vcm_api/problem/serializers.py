from rest_framework import serializers
from vcm_api.problem.models import Problem


class ProblemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = ['name', 'link', 'score']
