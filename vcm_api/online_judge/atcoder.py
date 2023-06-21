import requests


def check_solved(user_id, problem_id, contest_start_time, duration):
    """
    Check if the user has solved the problem.
    """

    url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={user_id}&from_second={contest_start_time}"  # noqa: E501
    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        # retry
        response = requests.get(url, timeout=5)

        response.raise_for_status()

    response = response.json()

    for submission in response:
        if submission["problem_id"] == problem_id and \
           submission["result"] == "AC" and \
           submission["epoch_second"] - contest_start_time <= duration:
            return True

    return False


def get_problem_id(problem_url):
    """
    Get the problem id from the problem url.
    """

    problem_id = problem_url.split("/")[-1]

    return problem_id
