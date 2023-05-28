from django.db import models
from vcm_api.contest.models import Contest


class Problem(models.Model):
    name = models.CharField(max_length=40)
    link = models.URLField(max_length=1000)
    score = models.PositiveIntegerField(default=100)
    contest = models.ForeignKey(Contest, related_name="problems",
                                blank=True, null=True, on_delete=models.CASCADE)
