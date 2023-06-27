import pytest
from vcm_api.problem import models


@pytest.mark.django_db
def test_problem_create_model_successful():
    models.Problem.objects.create(name="Is it Flower?",
                                  link="https://codeforces.com/problemset/problem/1811/F",
                                  score=100)
    assert models.Problem.objects.count() == 1


"""
    - put request to endpoint: /api/problem/:problemId
    - We have to check if this problem has been solved by the user or not
    - so the endpoint should have isAuthenticated permission
    - so check if the problem has been solved or not we would need 4 data points:
        i. user_id of the user on that specific problem's online judge
       ii. problem code of the problem
      iii. start_time of the contest
       iv. duration of the contest
    - to get i and ii we can store the online_judge on the Problem model
    - if we have the online judge we can retirieve i from the user's profile
                        (throw an error if the value is not available)
    - iii and iv can be obtained from the contest model
    - once we have this we can use the online_judge module to determine the verdict
    - then update the correct_answer field if required and respond the user
                with the required details
"""


@pytest.mark.django_db
def test_problemStatus_unauthenticatedUser_returnsForbidden():
    pass


@pytest.mark.django_db
def test_problemStatus_invalidProblemId_returnsBadRequest():
    pass


@pytest.mark.django_db
def test_ProblemStatus_authenticatedUserIsNotProblemOwner_returnsForbidden():
    pass


@pytest.mark.django_db
def test_ProblemStatus_noUserIdForProblemsOnlineJudge_returnsBadRequest():
    pass


@pytest.mark.django_db
def test_ProblemStatus_validRequest_problemUnSolved_returnSuccessfully():
    pass


@pytest.mark.django_db
def test_ProblemStatus_validRequest_problemSolved_returnSuccessfully():
    pass
