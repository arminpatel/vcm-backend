from codechef import Codechef


def test_check_solved():
    codechef = Codechef()

    # A user successfully submitted a solution to the problem at Wed Jun 21 2023 10:36:22 (IST)
    # we would test that

    assert not codechef.check_solved('sanu_sona', "LASTRBS", 1687321800, 0.5 * 3600)
    assert codechef.check_solved('sanu_sona', "LASTRBS", 1687321800, 2 * 3600)


def test_problem_id_retrieval_successful():
    codechef = Codechef()

    url = 'https://www.codechef.com/problems/ORXOR2'
    assert codechef.get_problem_id(url) == 'ORXOR2'
