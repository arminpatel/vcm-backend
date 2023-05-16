from django.db import models
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), primary_key=True, on_delete=models.CASCADE)
    cf_handle = models.CharField(max_length=100, unique=True)
    cc_handle = models.CharField(max_length=100, unique=True)
    ac_handle = models.CharField(max_length=100, unique=True)
