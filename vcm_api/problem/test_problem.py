import pytest
from vcm_api.problem import models


@pytest.mark.django_db
def test_problem_create_model_successful():
    models.Problem.objects.create(id="CF1811F", name="Is it Flower?",
                                  link="https://codeforces.com/problemset/problem/1811/F")
    assert models.Problem.objects.count() == 1
