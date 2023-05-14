import pytest
from django.contrib.auth import get_user_model
from vcm_api.user.models import Profile

User = get_user_model()

@pytest.mark.django_db
def test_user_creation_successful():
    User.objects.create(username="test_user123", first_name="test", last_name="user", password="test_me123")
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_user_and_profile_creation_successful():
    test_user = User.objects.create(username="test_user123", first_name="test", last_name="user", password="test_me123")
    Profile.objects.create(user=test_user, cc_handle="theoden42", cf_handle="0xarmin", ac_handle="theoden42")
    assert User.objects.count() == 1 and Profile.objects.count() == 1


@pytest.mark.django_db
def test_user_and_profile_deletion_cascade():
    test_user = User.objects.create(username="test_user123", first_name="test", last_name="user", password="test_me123")
    Profile.objects.create(user=test_user, cc_handle="theoden42", cf_handle="0xarmin", ac_handle="theoden42")
    test_user.delete()
    assert User.objects.count() == 0 and Profile.objects.count() == 0