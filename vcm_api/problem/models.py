from django.db import models
from django.contrib.auth import get_user_model


class Problem(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    name = models.CharField(max_length=40)
    link = models.URLField(max_length=1000)
    solved_by = models.ManyToManyField(get_user_model(), related_name="problems_solved")
