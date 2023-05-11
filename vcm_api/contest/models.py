from django.db import models
from vcm_api.problem.models import Problem


class Contest(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    start_date_time = models.DateTimeField()
    duration = models.DurationField()
    problems = models.ManyToManyField(Problem, related_name="appeared_in")
    # participants = models.ManyToManyField(
    #     get_user_model(), related_name="participated_in")
