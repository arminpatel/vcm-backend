from django.db import models
from django.contrib.auth import get_user_model
from vcm_api.contest.models import Contest
from vcm_api.problem.models import Problem


class Submission(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    time = models.DateTimeField()
    correct_answer = models.BooleanField()
