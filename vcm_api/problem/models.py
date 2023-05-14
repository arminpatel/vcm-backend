from django.db import models
from django.contrib.auth import get_user_model


class Problem(models.Model):
    id = models.CharField(max_length=40, primary_key=True, blank=False, null=False)
    name = models.CharField(max_length=40, blank=False, null=False)
    link = models.URLField(max_length=1000, blank=False, null=False)
    solved_by = models.ManyToManyField(get_user_model(), related_name="problems_solved")
