import pytest

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
