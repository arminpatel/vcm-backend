import pytest
from rest_framework import status
from rest_framework.test import APIClient
from vcm_api.contest.models import Contest
from vcm_api.problem.models import Problem
from django.contrib.auth import get_user_model

User = get_user_model()

contest_creation_body = {
    "name": "Test Contest",
    "start_date_time": "2021-09-01T00:00:00Z",
    "duration": "00:00:00",
    "problems": [
        {
            "name": "Test Problem 1",
            "link": "https://www.google.com",
            "score": 100,
            "online_judge": "codeforces"
        },
        {
            "name": "Test Problem 2",
            "link": "https://www.google.com",
            "score": 100,
            "online_judge": "codeforces"
        }
    ]
}


@pytest.fixture(scope='function')
def api_client():
    user = User.objects.create_user(username='john', email='js@js.com', password='js.sj')
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_create_contest_returns_201_created(api_client):
    response = api_client.post('/api/contests/', contest_creation_body, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Contest.objects.count() == 1
    assert Problem.objects.count() == 2
    assert Contest.objects.get().name == 'Test Contest'
    assert Contest.objects.get().participants.all().count() == 1
    assert Contest.objects.get().contest_creator.all().count() == 1


@pytest.mark.django_db
def test_create_contest_wihout_authentication_returns_401_unauthorized(api_client):
    api_client.force_authenticate(user=None)
    response = api_client.post('/api/contests/', contest_creation_body, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Contest.objects.count() == 0


@pytest.mark.parametrize("missing_field", ["name", "start_date_time", "duration", "problems"])
@pytest.mark.django_db
def test_create_contest_without_complete_contest_details_returns_HTTP_400_BAD_REQUEST(api_client, missing_field):  # noqa: E501
    value = contest_creation_body.pop(missing_field)
    response = api_client.post('/api/contests/', contest_creation_body, format='json')
    contest_creation_body[missing_field] = value

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Contest.objects.count() == 0
    assert Problem.objects.count() == 0


@pytest.mark.parametrize("problem_count", [0, 1])
@pytest.mark.parametrize("missing_field", ["problem.name", "problem.link", "problem.score"])
@pytest.mark.django_db
def test_create_contest_without_complete_problem_details_returns_HTTP_400_BAD_REQUEST(api_client, missing_field, problem_count):  # noqa: E501
    contest_creation_body["problems"][problem_count].pop(missing_field.split('.')[1])
    response = api_client.post('/api/contests/', contest_creation_body, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Contest.objects.count() == 0
    assert Problem.objects.count() == 0
