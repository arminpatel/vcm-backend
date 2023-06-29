from django.db import models
from django.contrib.auth import get_user_model
from vcm_api.problem.models import Problem


class Submission(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="submissions")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="submissions")
    time = models.DateTimeField()
    correct_answer = models.BooleanField()
