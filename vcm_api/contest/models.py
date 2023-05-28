from django.db import models
from django.contrib.auth import get_user_model


class Contest(models.Model):
    name = models.CharField(max_length=128)
    start_date_time = models.DateTimeField()
    duration = models.DurationField()
    participants = models.ManyToManyField(
        get_user_model(), related_name="participated_in")
    contest_creator = models.ManyToManyField(
        get_user_model(), related_name="contests_created")
