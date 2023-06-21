from vcm_api.online_judge.atcoder import get_problem_id


def test_get_problem_id():
    problem_url = "https://atcoder.jp/contests/abc001/tasks/abc001_1"
    assert get_problem_id(problem_url) == "abc001_1"
