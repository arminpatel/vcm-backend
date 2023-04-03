from django.db import models

class Problem(models.Model):
    id = models.CharField(max_length=20, blank=False, primary_key=True)
    name = models.CharField(max_length=128, blank=False)
    link = models.URLField(max_length=256, blank=False)

class Contest(models.Model):
    name = models.CharField(max_length=128, blank=False)
    start_date_time = models.DateTimeField()
    duration = models.DurationField()
    problems = models.ManyToManyField('Problem')


