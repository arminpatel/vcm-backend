import pytest
from vcm_api.contest.models import Contest
from vcm_api.problem.models import Problem
from datetime import timedelta, datetime
import pytz


@pytest.mark.django_db
def test_contest_create_model_successful():
    '''This tests successful creation of model'''

    test_problem = Problem.objects.create(
        id="CF1811F", name="Is it Flower?", link="https://codeforces.com/problemset/problem/1811/F")
    test_contest = Contest.objects.create(name="Good To Go", start_date_time=datetime(
        2022, 11, 23, 18, 55, 12, 23, tzinfo=pytz.UTC), duration=timedelta(hours=2, minutes=30))

    test_contest.problems.add(test_problem)
    assert Contest.objects.count() == 1
