import pytest
import pytz
from datetime import timedelta, datetime
from vcm_api.contest.models import Contest
from vcm_api.problem.models import Problem
from vcm_api.submission.models import Submission
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_submission_creation_successful():
    test_problem = Problem.objects.create(
        name="Is it Flower?", link="https://codeforces.com/problemset/problem/1811/F")
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

    test_submission = Submission.objects.create(user=test_user_participant,
                                                contest=test_contest,
                                                problem=test_problem,
                                                time=datetime(2022, 11, 23, 19, 10, 15, 27,
                                                              tzinfo=pytz.UTC), correct_answer=True)

    td = test_submission.time - test_submission.contest.start_date_time

    assert Submission.objects.count() == 1
    assert test_submission.contest.name == "Good To Go"

    assert td.days == 0 and td.seconds == 903 and td.microseconds == 4


@pytest.mark.django_db
def testSubmission_problemAndUserLinkedProperly():
    test_problem = Problem.objects.create(name="Is it Flower?",
                                          link="https://codeforces.com/problemset/problem/1811/F",
                                          score=100)

    test_contest = Contest.objects.create(name="Good To Go", start_date_time=datetime(
        2022, 11, 23, 18, 55, 12, 23, tzinfo=pytz.UTC), duration=timedelta(hours=2, minutes=30))

    test_contest.problems.add(test_problem)

    test_user = User.objects.create(
        first_name="test", last_name="user-1", username="theoden42", password="test_me123")

    Submission.objects.create(user=test_user,
                              contest=test_contest,
                              problem=test_problem,
                              time=datetime(2022, 11, 23, 19, 10, 15, 27,
                                            tzinfo=pytz.UTC), correct_answer=True)

    assert Submission.objects.count() == 1
    assert test_problem.submissions.count() == 1
    assert test_user.submissions.count() == 1
    assert test_user.submissions.first().problem == test_problem
