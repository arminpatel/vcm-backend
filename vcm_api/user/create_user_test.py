import pytest

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
def testCreateUser_correctUserDetails_creationSuccess():
    # Arrange
    client = APIClient()

    # Act
    response = client.post('/api/users/', {
                           'username': 'testuser',
                           'password': 'testpass',
                           'first_name': 'test',
                           'last_name': 'user',
                           })

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert response.data == {
            'username': 'testuser',
            'first_name': 'test',
            'last_name': 'user',
            'profile': {
                'cf_handle': None,
                'cc_handle': None,
                'ac_handle': None,
            },
        }

    assert User.objects.first().username == 'testuser'
    # Password should be hashed
    assert User.objects.first().password != 'testpass'


@pytest.mark.django_db
@pytest.mark.parametrize('required_field', [
    'username',
    'password',
])
def testCreateUser_missingRequiredField_returnsBadRequest(required_field):
    # Arrange
    client = APIClient()
    data = {
        'username': 'testuser',
        'password': 'testpass',
        'first_name': 'test',
        'last_name': 'user',
    }
    del data[required_field]

    # Act
    response = client.post('/api/users/', data)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0


@pytest.mark.django_db
def testCreateUser_duplicateUsername_returnsBadRequest():
    # Arrange
    client = APIClient()
    User.objects.create_user(
        username='testuser',
        password='testpass',
        first_name='test',
        last_name='user',
    )

    # Act
    response = client.post('/api/users/', {
                           'username': 'testuser',
                           'password': 'testpass',
                           'first_name': 'test',
                           'last_name': 'user',
                           })

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 1
