import pytest
from collections import OrderedDict
from rest_framework import status
from rest_framework.test import APIClient
from vcm_api.contest.models import Contest
from vcm_api.problem.models import Problem
import pytz
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model


@pytest.fixture
@pytest.mark.django_db
def test_contest():
    problem1 = Problem.objects.create(name="someproblem1",
                                      link="https://somelink.com",
                                      score=100,
                                      online_judge="codeforces")
    problem2 = Problem.objects.create(name='someproblem2',
                                      link="https://somelink.com",
                                      score=300,
                                      online_judge="codeforces")
    test_contest = Contest.objects.create(name="Good To Go", start_date_time=datetime(
        2022, 11, 23, 18, 55, 12, 23, tzinfo=pytz.UTC), duration=timedelta(hours=2, minutes=30))

    test_contest.problems.add(problem1, problem2)
    return test_contest


@pytest.fixture
@pytest.mark.django_db
def test_contest2():
    problem3 = Problem.objects.create(name='someproblem3',
                                      link="https://somelink.com",
                                      score=200,
                                      online_judge="codeforces")
    test_contest2 = Contest.objects.create(name="Good To Go2", start_date_time=datetime(
        2022, 11, 23, 18, 55, 12, 23, tzinfo=pytz.utc), duration=timedelta(hours=2, minutes=30))

    test_contest2.problems.add(problem3)
    return test_contest2


@pytest.mark.django_db
def test_listcontestview_successful_return_200_ok(test_contest, test_contest2):
    '''this test creates a contest in the past and therefore recieves a response
    with all the problems from the contest'''

    # arrange
    client = APIClient()
    user = get_user_model()

    test_user_participant = user.objects.create(
        first_name="test", last_name="user-1", username="theoden42", password="test_me123")

    test_contest.participants.add(test_user_participant)
    test_contest2.participants.add(test_user_participant)

    # act
    response = client.get('/api/contests/user/theoden42/', format="json")

    # assert
    assert response.status_code == status.HTTP_200_OK

    assert response.data == [
        OrderedDict([('id', 1), ('name', 'Good To Go'),
                     ('start_date_time', '2022-11-23T18:55:12.000023Z'),
                     ('duration', '02:30:00'),
                     ('problems', [
                         OrderedDict(
                             [('id', 1),
                              ('name', 'someproblem1'),
                              ('link', 'https://somelink.com'),
                              ('score', 100),
                              ('online_judge', 'codeforces'),
                              ('is_solved', False)
                              ]),
                         OrderedDict(
                             [('id', 2),
                              ('name', 'someproblem2'),
                              ('link', 'https://somelink.com'),
                              ('score', 300),
                              ('online_judge', 'codeforces'),
                              ('is_solved', False)
                              ])
                     ]
        )]),
        OrderedDict([('id', 2), ('name', 'Good To Go2'),
                     ('start_date_time', '2022-11-23T18:55:12.000023Z'),
                     ('duration', '02:30:00'),
                     ('problems', [
                         OrderedDict(
                             [('id', 3),
                              ('name', 'someproblem3'),
                              ('link', 'https://somelink.com'),
                              ('score', 200),
                              ('online_judge', 'codeforces'),
                              ('is_solved', False)
                              ])
                     ]
        )]),
    ]


@pytest.mark.django_db
def test_ListContestView_user_does_not_exist_returns_404_NOT_FOUND():

    # Arrange
    client = APIClient()
    User = get_user_model()
    User.objects.create(
        first_name="test", last_name="user-1", username="theoden42", password="test_me123")

    # Act
    response = client.get('/api/contests/user/test_user_incorrect/', format="json")
    response2 = client.get('/api/contests/user/theoden42/')

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response2.status_code == status.HTTP_200_OK
    assert response2.data == []


@pytest.mark.django_db
def test_Retrieve_one_ContestView_successful_returns_200_OK(test_contest):

    # Arrange
    client = APIClient()
    # Act
    response = client.get('/api/contests/1/', format="json")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data == OrderedDict([('id', 1), ('name', 'Good To Go'),
                                         ('start_date_time', '2022-11-23T18:55:12.000023Z'),
                                         ('duration', '02:30:00'),
                                         ('problems', [
                                             OrderedDict(
                                                 [('id', 1),
                                                  ('name', 'someproblem1'),
                                                  ('link', 'https://somelink.com'),
                                                  ('score', 100),
                                                  ('online_judge', 'codeforces'),
                                                  ('is_solved', False)
                                                  ]),
                                             OrderedDict(
                                                 [('id', 2),
                                                  ('name', 'someproblem2'),
                                                  ('link', 'https://somelink.com'),
                                                  ('score', 300),
                                                  ('online_judge', 'codeforces'),
                                                  ('is_solved', False)
                                                  ])
                                         ]
    )])


@pytest.mark.django_db
def test_RetrieveContestView_contest_id_is_incorrect_returns_404_NOT_FOUND():

    # Arrange
    client = APIClient()
    # Act
    response = client.get('/api/contests/2/', format="json")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_contest_list_view_starting_time_in_future_doesnot_return_problems_succesful(test_contest, test_contest2):  # noqa: E501

    User = get_user_model()
    test_user_participant = User.objects.create(
        first_name="test", last_name="user-1", username="theoden42", password="test_me123")

    test_contest.participants.add(test_user_participant)
    test_contest2.participants.add(test_user_participant)

    later_time = datetime.now(pytz.UTC) + timedelta(days=1)

    test_contest.start_date_time = later_time
    test_contest.save()
    test_contest2.start_date_time = later_time
    test_contest2.save()

    client = APIClient()

    response = client.get('/api/contests/user/theoden42/', format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        OrderedDict([('id', 1), ('name', 'Good To Go'),
                     ('start_date_time', later_time.isoformat().split('+')[0] + 'Z'),
                     ('duration', '02:30:00'),
                     ('problems', [])
                     ]),
        OrderedDict([('id', 2), ('name', 'Good To Go2'),
                     ('start_date_time', later_time.isoformat().split('+')[0] + 'Z'),
                     ('duration', '02:30:00'),
                     ('problems', [])
                     ]),
    ]


@pytest.mark.django_db
def test_contest_retrieval_starting_time_in_future_doesnot_return_problems_succesful(test_contest):

    later_time = datetime.now(pytz.UTC) + timedelta(days=1)
    test_contest.start_date_time = later_time
    test_contest.save()

    client = APIClient()

    response = client.get('/api/contests/1/', format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data == OrderedDict([('id', 1), ('name', 'Good To Go'),
                                         ('start_date_time',
                                          later_time.isoformat().split('+')[0] + 'Z'),
                                         ('duration', '02:30:00'),
                                         ('problems', [])
                                         ])
