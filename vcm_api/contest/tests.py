import pytest
from vcm_api.contest import models
from datetime import timedelta, datetime
import pytz


@pytest.mark.django_db
def test_contest_create_model_successful():
    models.Contest.objects.create(name="Good To Go", start_date_time=datetime(
        2022, 11, 23, 18, 55, 12, 23, tzinfo=pytz.UTC), duration=timedelta(hours=2, minutes=30))
    assert models.Contest.objects.count() == 1
