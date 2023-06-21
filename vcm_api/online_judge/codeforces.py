import requests


def check_solved(user, problem_id, contest_start_time, duration):
    # assuming contest_start_time and duration is in seconds
    """
        check if a particular problem is solved by a user before starting the contest
    """
    url = f"https://codeforces.com/api/user.status?handle={user}&from=1&count=100000"
    response = requests.get(url, timeout=5)
    response = response.json()

    if response["status"] != "OK":
        # retry
        response = requests.get(url, timeout=5)
        response = response.json()

        if response["status"] != "OK":
            raise Exception("Could not reach Codeforces API")

    # check each submission if it is accepted and is in the contest time
    for submission in response["result"]:
        submission_problem_id = str(submission["problem"]["contestId"]) + \
            submission["problem"]["index"]
        if submission["verdict"] == "OK" and \
           submission_problem_id == problem_id and \
           submission["creationTimeSeconds"] >= contest_start_time and \
           submission["creationTimeSeconds"] <= contest_start_time + duration:
            return True

        # if the submission is before the contest start time, break
        if submission["creationTimeSeconds"] < contest_start_time:
            break

    return False


def get_problem_id(problem_url):
    """
        get problem id from problem url
    """
    # problem url is of the form: https://codeforces.com/contest/1360/problem/A
    problem_url = problem_url.split("/")
    problem_id = problem_url[-3] + problem_url[-1]

    return problem_id


def convert_problem_url(problem_url):
    """
        convert problem url to the form: https://codeforces.com/contest/1360/problem/A
    """
    problem_url_split = problem_url.split("/")
    if problem_url_split[3] == "contest" or \
       problem_url_split[3] == "gym" or \
       problem_url_split[4] == "acmsguru":
        return problem_url

    return f"https://codeforces.com/contest/{problem_url_split[-2]}/problem/{problem_url_split[-1]}"
