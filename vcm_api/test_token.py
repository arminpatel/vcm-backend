from datetime import timedelta
import pytest
import time

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture
def api_client():
    user = User.objects.create(username="armin", email="a@a.com")
    user.set_password('123armin')
    user.save()
    client = APIClient()

    return client


@pytest.mark.django_db
def testToken_correctUserCredentials_tokenSuccussfullyReturned(api_client):
    response = api_client.post("http://localhost:8000/api/token/", {
                                   "username": "armin",
                                   "password": "123armin"
                               })

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def testToken_wrongUserCredentials_returnsUnauthorized(api_client):
    response = api_client.post("http://localhost:8000/api/token/", {
                                   "username": "armin",
                                   "password": "wrong"
                               })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def testToken_correctToken_verificationSuccessfull(api_client):
    response = api_client.post("http://localhost:8000/api/token/", {
                                   "username": "armin",
                                   "password": "123armin"
                               })
    assert response.status_code == status.HTTP_200_OK

    response = api_client.post("https://localhost:8000/api/token/verify/", {
                                    "token": response.data["access"]
                                })

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def testToken_wrongToken_returnsUnautorized(api_client):
    response = api_client.post("https://localhost:8000/api/token/verify/", {
                                    "token": "wrong token here obviously"
                                })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def testToken_refreshToken_correctRefreshToken_returnsSucessfully(api_client):
    response = api_client.post("http://localhost:8000/api/token/", {
                                   "username": "armin",
                                   "password": "123armin"
                               })

    assert response.status_code == status.HTTP_200_OK

    response = api_client.post("http://localhost:8000/api/token/refresh/", {
                                   "refresh": response.data['refresh']
                               })

    assert response.status_code == status.HTTP_200_OK

    response = api_client.post("https://localhost:8000/api/token/verify/", {
                                    "token": response.data['access']
                                })

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def testToken_refreshToken_wrongRefreshToken_returnsUnauthorized(api_client):
    response = api_client.post("http://localhost:8000/api/token/refresh/", {
                                   "refresh": "wrong token obviously"
                               })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
