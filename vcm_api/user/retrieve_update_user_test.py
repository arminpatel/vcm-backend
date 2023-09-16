import pytest
from collections import OrderedDict

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from vcm_api.user.models import Profile

User = get_user_model()


@pytest.mark.django_db
def testRetrieveUserView_invalidUsername_returnsNotFound():
    # Arrange
    client = APIClient()

    # Act
    response = client.get('/api/users/invalidUsername/')

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def testRetrieveUserView_validUsername_returnsSuccessfully():
    # Arrange
    client = APIClient()
    user = User.objects.create(username='testUsername')
    Profile.objects.create(user=user, cf_handle='testCFHandle',
                           cc_handle='testCCHandle')

    # Act
    response = client.get('/api/users/testUsername/')

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
                             'username': 'testUsername',
                             'first_name': '',
                             'last_name': '',
                             'profile': {
                                'cf_handle': 'testCFHandle',
                                'cc_handle': 'testCCHandle',
                                'ac_handle': None,
                                }
                            }


@pytest.mark.django_db
def testUpdateUserView_invalidUsername_returnsNotFound():
    # Arrange
    client = APIClient()

    # Act
    response = client.put('/api/users/invalidUsername/',
                          {'first_name': 'testFirstName',
                           'last_name': 'testLastName'})

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def testUpdateUserView_validUsername_notLoggedIn_returnsUnauthorized():
    # Arrange
    client = APIClient()
    User.objects.create(username='testUsername')

    # Act
    response = client.put('/api/users/testUsername/', {})

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def testUpdateUserView_validUsername_notOwner_returnsForbidden():
    # Arrange
    client = APIClient()
    User.objects.create(username='testUsername')
    client.force_authenticate(user=User.objects.create(username='testUsername2'))

    # Act
    response = client.put('/api/users/testUsername/', {})

    # Assert
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def testUpdateUserView_validUsername_ownerRequest_updateSuccessful():
    # Arrange
    client = APIClient()

    client.post('/api/users/', {'username': 'testUsername', 'password': 'testPassword'})
    user = User.objects.get(username='testUsername')

    client.force_authenticate(user=user)

    # Act
    response = client.put('/api/users/testUsername/',
                          {'first_name': 'testFirstName',
                           'last_name': 'testLastName',
                           'profile': {
                                'cf_handle': 'testCFHandle'
                           }}, format='json')
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        'first_name': 'testFirstName',
        'last_name': 'testLastName',
        'profile': OrderedDict([('cf_handle', 'testCFHandle'),
                                ('cc_handle', None),
                                ('ac_handle', None)]),
        'username': 'testUsername'
    }


@pytest.mark.django_db
def testUpdateUserView_validUsername_adminRequest_updateSuccessful():
    # Arrange
    client = APIClient()

    client.post('/api/users/', {'username': 'testUsername', 'password': 'testPassword'})
    User.objects.get(username='testUsername')

    client.force_authenticate(user=User.objects.create(username='testUsername2', is_staff=True))

    # Act
    response = client.put('/api/users/testUsername/',
                          {'first_name': 'testFirstName',
                           'last_name': 'testLastName',
                           'profile': {
                                'cf_handle': 'testCFHandle'
                           }}, format='json')
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        'first_name': 'testFirstName',
        'last_name': 'testLastName',
        'profile': OrderedDict([('cf_handle', 'testCFHandle'),
                                ('cc_handle', None),
                                ('ac_handle', None)]),
        'username': 'testUsername'
    }
