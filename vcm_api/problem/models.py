from django.db import models


class Problem(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    name = models.CharField(max_length=40)
    link = models.URLField(max_length=1000)
