import pytest
import pytz
from datetime import timedelta, datetime
from vcm_api.contest.models import Contest
from vcm_api.problem.models import Problem
from vcm_api.user.models import Profile
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


@pytest.fixture
@pytest.mark.django_db
def test_user():
    '''This fixture provides the test with user along with profile'''
    test_user = User.objects.create(
        first_name="test",
        last_name="user",
        username="gibberish",
        password="test_me123")
    return test_user


@pytest.fixture
@pytest.mark.django_db
def test_profile():
    '''This fixture provides the test with a profile with valid online_judge usernames'''
    test_profile = Profile.objects.create(
        cf_handle="gtheoden42",
        cc_handle="theoden42",
        ac_handle="gtheoden42")
    return test_profile


@pytest.fixture
@pytest.mark.django_db
def test_contest():
    '''This fixture provides the test with test contest with valid problems'''
    test_problem1 = Problem.objects.create(
        name="PermuTree",
        link="https://codeforces.com/problemset/problem/1856/E1",
        score=100,
        online_judge="codeforces")
    test_problem2 = Problem.objects.create(
        name="TwoPiles",
        link="https://www.codechef.com/problems/SPLITMIN",
        score=100,
        online_judge="codechef")
    test_problem3 = Problem.objects.create(
        name="Odd or Even",
        link="https://atcoder.jp/contests/abc313/tasks/abc313_d",
        score=100,
        online_judge="atcoder")

    test_contest = Contest.objects.create(name="CodeRumble", start_date_time=datetime(
        2023, 8, 9, 12, 0, 0, 0, tzinfo=pytz.UTC), duration=timedelta(hours=5, minutes=30))
    test_contest.problems.add(test_problem1)
    test_contest.problems.add(test_problem2)
    test_contest.problems.add(test_problem3)
    return test_contest


@pytest.mark.django_db
def test_problemStatus_unauthenticatedUser_returns_unauthorized():
    client = APIClient()
    uri = '/api/submissions/'
    response = client.post(uri, {"problem_id": 1})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_problemStatus_invalidProblemId_returns_bad_request(test_user):
    client = APIClient()
    uri = '/api/submissions/'
    client.force_authenticate(user=test_user)
    response = client.post(uri, {"problem_id": '101001'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_ProblemStatus_authenticatedUserIsNotProblemOwnerOrParticipantOrAdmin_returns_forbidden(
        test_contest, test_user):
    client = APIClient()
    client.force_authenticate(user=test_user)
    uri = '/api/submissions/'
    response = client.post(uri, {"problem_id": 1})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize('online_judge', ['codeforces', 'codechef', 'atcoder'])
def test_ProblemStatus_noUserIdForProblemsOnlineJudge_returnsBadRequest(
        online_judge, test_contest, test_user, test_profile):
    client = APIClient()
    client.force_authenticate(user=test_user)
    problem_id = 1

    if online_judge == 'codeforces':
        test_profile.cf_handle = None
        problem_id = 1
    elif online_judge == 'codechef':
        test_profile.cc_handle = None
        problem_id = 2
    else:
        test_profile.ac_handle = None
        problem_id = 3

    test_user.profile = test_profile
    test_contest.participants.add(test_user)
    uri = '/api/submissions/'
    response = client.post(uri, {"problem_id": problem_id})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content.decode('utf-8') == f'["{online_judge} handle is not available"]'


@pytest.mark.django_db
@pytest.mark.parametrize('online_judge', ['codeforces', 'codechef', 'atcoder'])
def test_ProblemStatus_validRequest_problemUnSolved_returnsBad_Request(
        online_judge, test_user, test_profile, test_contest):
    client = APIClient()
    client.force_authenticate(user=test_user)
    problem_id = 1

    if online_judge == 'codeforces':
        test_profile.cf_handle = 'tourist'
        problem_id = 1
    elif online_judge == 'codechef':
        test_profile.cc_handle = 'gennady.korotkevich'
        problem_id = 2
    else:
        test_profile.ac_handle = 'tourist'
        problem_id = 3

    test_user.profile = test_profile
    test_contest.participants.add(test_user)
    uri = '/api/submissions/'
    response = client.post(uri, {"problem_id": problem_id})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content.decode('utf-8') == '["problem is not solved"]'


@pytest.mark.django_db
@pytest.mark.parametrize('problem_id', [1, 2, 3])
def test_ProblemStatus_validRequest_ContestOwner_problemSolved_returnSuccessfully(
        problem_id, test_user, test_profile, test_contest):
    client = APIClient()
    client.force_authenticate(user=test_user)
    test_user.profile = test_profile
    test_contest.contest_creator.add(test_user)
    uri = '/api/submissions/'
    response = client.post(uri, {"problem_id": problem_id})
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
@pytest.mark.parametrize('problem_id', [1, 2, 3])
def test_ProblemStatus_validRequest_ContestParticipant_problemSolved_returnSuccessfully(  # noqa: E501
        problem_id, test_user, test_profile, test_contest):
    client = APIClient()
    client.force_authenticate(user=test_user)
    test_user.profile = test_profile
    test_contest.participants.add(test_user)
    uri = '/api/submissions/'
    response = client.post(uri, {"problem_id": problem_id})
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
@pytest.mark.parametrize('problem_id', [1, 2, 3])
def test_ProblemStatus_validRequest_Admin_problemSolved_returnSuccessfully(  # noqa: E501
        problem_id, test_user, test_profile, test_contest):
    client = APIClient()
    client.force_authenticate(user=test_user)
    test_user.profile = test_profile
    test_user.is_staff = True
    uri = '/api/submissions/'
    response = client.post(uri, {"problem_id": problem_id})
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
@pytest.mark.parametrize('problem_id', [1, 2, 3])
def test_ProblemStatus_is_solved_is_true_in_get_contest_view_response_after_successful_submission(
        problem_id, test_user, test_profile, test_contest):
    client = APIClient()
    client.force_authenticate(user=test_user)
    test_user.profile = test_profile
    test_contest.participants.add(test_user)
    uri1 = '/api/submissions/'
    response = client.post(uri1, {"problem_id": problem_id})
    assert response.status_code == status.HTTP_201_CREATED
    # get the problems from the contest view and check if the status of the
    # problem is correctly identified
    uri2 = '/api/contests/1/'
    response = client.get(uri2, format="json")
    assert response.status_code == status.HTTP_200_OK
    response_problems = response.data.pop("problems")

    for problem in response_problems:
        if problem['id'] != problem_id:
            assert not problem['is_solved']
        else:
            assert problem['is_solved']
