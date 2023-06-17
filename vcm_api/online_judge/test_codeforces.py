from vcm_api.online_judge import codeforces
import pytest

# check_solved function is checked manually for now


@pytest.mark.parametrize(
    "problem_url, expected",
    [
        ("https://codeforces.com/contest/4/problem/A",
         "https://codeforces.com/contest/4/problem/A"),
        ("https://codeforces.com/problemset/problem/4/A",
         "https://codeforces.com/contest/4/problem/A"),
        ("https://codeforces.com/gym/102644/problem/A",
         "https://codeforces.com/gym/102644/problem/A"),
        ("https://codeforces.com/problemsets/acmsguru/problem/99999/99999",
         "https://codeforces.com/problemsets/acmsguru/problem/99999/99999")
    ]
)
def test_problem_url_conversion(problem_url, expected):
    new_problem_url = codeforces.convert_problem_url(problem_url)

    assert new_problem_url == expected


def test_get_problem_id():
    problem_url = "https://codeforces.com/contest/4/problem/A"

    problem_id = codeforces.get_problem_id(problem_url)

    assert problem_id == "4A"
