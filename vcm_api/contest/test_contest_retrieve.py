import pytest
from collections import OrderedDict
from rest_framework import status
from rest_framework.test import APIClient
from vcm_api.contest.models import Contest
from vcm_api.problem.models import Problem
import pytz
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_ListContestView_successful():

    # Arrange
    client = APIClient()
    User = get_user_model()

    problem1 = Problem.objects.create(name="someproblem1", link="somelink.com", score=100)
    problem2 = Problem.objects.create(name='someproblem2', link="somelink.com", score=300)
    problem3 = Problem.objects.create(name='someproblem3', link="somelink.com", score=200)
    test_user_participant = User.objects.create(
        first_name="test", last_name="user-1", username="theoden42", password="test_me123")

    test_contest = Contest.objects.create(name="Good To Go", start_date_time=datetime(
        2022, 11, 23, 18, 55, 12, 23, tzinfo=pytz.UTC), duration=timedelta(hours=2, minutes=30))

    test_contest2 = Contest.objects.create(name="Good To Go2", start_date_time=datetime(
        2022, 11, 23, 18, 55, 12, 23, tzinfo=pytz.UTC), duration=timedelta(hours=2, minutes=30))

    test_contest.problems.add(problem1, problem2)
    test_contest2.problems.add(problem3)
    test_contest.participants.add(test_user_participant)
    test_contest2.participants.add(test_user_participant)

    # Act
    response = client.get('/api/contests/user/theoden42', format="json")

    # Assert
    assert response.status_code == status.HTTP_200_OK

    assert response.data == [
        OrderedDict([('id', 1), ('name', 'Good To Go'),
                     ('start_date_time', '2022-11-23T18:55:12.000023Z'),
                     ('duration', '02:30:00'),
                     ('problems', [
                         OrderedDict(
                             [('name', 'someproblem1'),
                              ('link', 'somelink.com'),
                              ('score', 100)]),
                         OrderedDict(
                             [('name', 'someproblem2'),
                              ('link', 'somelink.com'),
                              ('score', 300)])
                     ]
        )]),
        OrderedDict([('id', 2), ('name', 'Good To Go2'),
                     ('start_date_time', '2022-11-23T18:55:12.000023Z'),
                     ('duration', '02:30:00'),
                     ('problems', [
                         OrderedDict(
                             [('name', 'someproblem3'),
                              ('link', 'somelink.com'),
                              ('score', 200)])]
                      )])
    ]


@pytest.mark.django_db
def test_ListContestView_unsuccessful():

    # Arrange
    client = APIClient()
    User = get_user_model()
    User.objects.create(
        first_name="test", last_name="user-1", username="theoden42", password="test_me123")

    # Act
    response = client.get('/api/contests/user/test_user_incorrect', format="json")
    response2 = client.get('/api/contests/user/theoden42')

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response2.status_code == status.HTTP_200_OK
    assert response2.data == []


@pytest.mark.django_db
def test_RetrieveContestView_successful():

    # Arrange
    client = APIClient()
    problem1 = Problem.objects.create(name="someproblem1", link="somelink.com", score=100)
    problem2 = Problem.objects.create(name='someproblem2', link="somelink.com", score=300)

    test_contest = Contest.objects.create(name="Good To Go", start_date_time=datetime(
        2022, 11, 23, 18, 55, 12, 23, tzinfo=pytz.UTC), duration=timedelta(hours=2, minutes=30))

    test_contest.problems.add(problem1, problem2)

    # Act
    response = client.get('/api/contests/1', format="json")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data == OrderedDict([('id', 1), ('name', 'Good To Go'),
                                         ('start_date_time', '2022-11-23T18:55:12.000023Z'),
                                         ('duration', '02:30:00'),
                                         ('problems', [
                                             OrderedDict(
                                                 [('name', 'someproblem1'),
                                                  ('link', 'somelink.com'),
                                                  ('score', 100)]),
                                             OrderedDict(
                                                 [('name', 'someproblem2'),
                                                  ('link', 'somelink.com'),
                                                  ('score', 300)])
                                         ]
    )])


@pytest.mark.django_db
def test_RetrieveContestView_unsuccessful():

    # Arrange
    client = APIClient()
    # Act
    response = client.get('/api/contests/2', format="json")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
