from django.db import models
from vcm_api.contest.models import Contest


class Problem(models.Model):
    ONLINE_JUDGE_CHOICES = (
        ('codeforces', 'Codeforces'),
        ('codechef', 'Codechef'),
        ('atcoder', 'Atcoder'),
    )

    name = models.CharField(max_length=40)
    link = models.URLField(max_length=1000)
    score = models.PositiveIntegerField(default=100)
    contest = models.ForeignKey(Contest, related_name="problems",
                                blank=True, null=True, on_delete=models.CASCADE)
    online_judge = models.CharField(max_length=20, choices=ONLINE_JUDGE_CHOICES, blank=False)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
