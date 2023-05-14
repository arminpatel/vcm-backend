from django.contrib import admin
from user.models import Profile
from contest.models import Contest
from problem.models import Problem

# Register your models here.10
admin.site.register(Problem)
admin.site.register(Contest)
admin.site.register(Profile)
