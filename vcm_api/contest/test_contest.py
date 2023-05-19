from django.contrib.auth import get_user_model
from vcm_api.contest.models import Contest
from vcm_api.problem.models import Problem
from datetime import timedelta, datetime
import pytz
import pytest

User = get_user_model()


@pytest.mark.django_db
def test_contest_create_model_successful():
    '''This tests successful creation of model'''

    test_problem = Problem.objects.create(
        id="CF1811F", name="Is it Flower?",
        link="https://codeforces.com/problemset/problem/1811/F", score=100)

    test_contest = Contest.objects.create(name="Good To Go", start_date_time=datetime(
        2022, 11, 23, 18, 55, 12, 23, tzinfo=pytz.UTC), duration=timedelta(hours=2, minutes=30))

    test_contest.problems.add(test_problem)
    assert Contest.objects.count() == 1


@pytest.mark.django_db
def test_contest_can_access_problem_succesful():

    test_problem = Problem.objects.create(
        id="CF1811F", name="Is it Flower?",
        link="https://codeforces.com/problemset/problem/1811/F", score=100)

    test_contest = Contest.objects.create(name="Good To Go", start_date_time=datetime(
        2022, 11, 23, 18, 55, 12, 23, tzinfo=pytz.UTC), duration=timedelta(hours=2, minutes=30))

    test_contest.problems.add(test_problem)

    for problem in test_contest.problems.all():
        assert problem.name == "Is it Flower?"


@pytest.mark.django_db
def test_contest_link_with_user_successful():
    '''This tests if the contest creator field and particpant field are linked'''

    test_problem = Problem.objects.create(
        id="CF1811F", name="Is it Flower?",
        link="https://codeforces.com/problemset/problem/1811/F", score=100)
    test_contest = Contest.objects.create(name="Good To Go", start_date_time=datetime(
        2022, 11, 23, 18, 55, 12, 23, tzinfo=pytz.UTC), duration=timedelta(hours=2, minutes=30))

    test_user_participant = User.objects.create(
        first_name="test", last_name="user-1", username="theoden42", password="test_me123")
    test_user_manager = User.objects.create(
        first_name="test", last_name="user-2", username="0xarmin", password="test_me789")

    test_contest.problems.add(test_problem)
    test_contest.participants.add(test_user_participant)
    test_contest.contest_creator.add(test_user_manager)

    assert Contest.objects.count() == 1

    for user in test_contest.participants.all():
        assert (user.first_name == "test" and
                user.last_name == "user-1" and user.username == "theoden42")

    for user in test_contest.contest_creator.all():
        assert (user.first_name == "test" and
                user.last_name == "user-2" and user.username == "0xarmin")

    for contest in test_user_participant.participated_in.all():
        assert (contest.name == "Good To Go")

    for contest in test_user_manager.contests_created.all():
        assert (contest.name == "Good To Go")
