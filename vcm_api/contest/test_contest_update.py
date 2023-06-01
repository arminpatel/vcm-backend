import pytest
import pytz
from vcm_api.contest.models import Contest
from vcm_api.problem.models import Problem
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta

User = get_user_model()
data = {
    'name': 'nottestcontest',
    'start_date_time': '2022-07-06T00:00:00Z',
    'duration': '02:00:00',
    'problems': [
        {
            'link': 'https://www.codechef.com/problems/TEST3',
            'name': 'TEST3',
            'score': 100
        }
    ]
}


@pytest.fixture(scope='function')
@pytest.mark.django_db
def created_contest():
    problem1 = Problem.objects.create(
        link='https://www.codechef.com/problems/TEST', name='TEST', score=100)
    problem2 = Problem.objects.create(
        link='https://www.codechef.com/problems/TEST2', name='TEST2', score=100)
    contest = Contest.objects.create(name='testcontest', start_date_time=datetime(
        2022, 11, 23, 18, 55, 12, 23, tzinfo=pytz.UTC), duration=timedelta(hours=2, minutes=30))
    contest.problems.add(problem1)
    contest.problems.add(problem2)
    return contest


@pytest.mark.django_db
def test_contest_update_all_details_successful_returns_200(created_contest):

    test_user = User.objects.create(first_name='test', last_name='user',
                                    username='testuser', password='something')
    client = APIClient()
    client.force_authenticate(user=test_user)
    created_contest.contest_creator.add(test_user)

    id = created_contest.id
    uri = f'/api/contests/{id}/'
    response = client.put(uri, data=data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert Contest.objects.get(id=id).name == 'nottestcontest'
    assert Contest.objects.get(id=id).start_date_time == datetime(
        2022, 7, 6, 00, 00, 00, 00, tzinfo=pytz.UTC)
    assert Contest.objects.get(id=id).duration == timedelta(hours=2)
    assert Contest.objects.get(id=id).problems.count() == 1
    assert (Contest.objects.get(id=id).problems.first().link
            == 'https://www.codechef.com/problems/TEST3')


@pytest.mark.django_db
@pytest.mark.parametrize('value_to_update', ['name', 'start_date_time', 'duration'])
def test_contest_update_one_detail_successful_returns_200(created_contest, value_to_update):

    test_user = User.objects.create(first_name='test', last_name='user',
                                    username='testuser', password='something')
    client = APIClient()
    client.force_authenticate(user=test_user)
    created_contest.contest_creator.add(test_user)

    id = created_contest.id
    uri = f'/api/contests/{id}/'
    new_data = {
        value_to_update: data.get(value_to_update)
    }
    response = client.patch(uri, data=new_data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get(value_to_update) == data.get(value_to_update)


@pytest.mark.django_db
def test_contest_update_old_problems_to_new_problems_successful_returns_200(created_contest):

    test_user = User.objects.create(first_name='test', last_name='user',
                                    username='testuser', password='something')
    client = APIClient()
    client.force_authenticate(user=test_user)
    created_contest.contest_creator.add(test_user)

    id = created_contest.id
    uri = f'/api/contests/{id}/'
    new_data = {
        'problems': [
            {
                'link': 'https://www.codechef.com/problems/TEST3',
                'name': 'TEST3',
                'score': 100
            },
            {
                'link': 'https://www.codechef.com/problems/TEST',
                'name': 'TEST',
                'score': 100

            }
        ]
    }
    response = client.patch(uri, data=new_data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert Contest.objects.get(id=id).problems.count() == 2
    assert Problem.objects.all().count() == 2
    assert not Problem.objects.filter(link='https://www.codechef.com/problems/TEST2').exists()
    assert Problem.objects.filter(link='https://www.codechef.com/problems/TEST').exists()


@pytest.mark.django_db
def test_user_not_contest_creator_update_contest_request_returns_403_forbidden(created_contest):

    test_user = User.objects.create(first_name='test', last_name='user',
                                    username='testuser', password='something')
    client = APIClient()
    client.force_authenticate(user=test_user)

    id = created_contest.id
    uri = f'/api/contests/{id}/'
    response = client.put(uri, data=data, format='json')

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_not_authenticated_update_contest_request_returns_401_unauthorized(created_contest):

    client = APIClient()
    id = created_contest.id
    uri = f'/api/contests/{id}/'
    response = client.put(uri, data=data, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_contes_does_not_exist_update_request_returns_404_not_found():
    client = APIClient()
    client.force_authenticate(user=User.objects.create(
        first_name='test', last_name='user', username='testuser', password='something'))
    uri = '/api/contests/1/'
    response = client.put(uri, data=data, format='json')

    assert response.status_code == status.HTTP_404_NOT_FOUND
