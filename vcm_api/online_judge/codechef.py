import datetime
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver


class Codechef:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1200")
        self.driver = webdriver.Chrome(options=options)

    def check_solved(self, user, problem_code, contest_start_time, duration):
        # Assuming constest_start_time and duration is in seconds
        """
        Check if a user has solved a problem in a contest
        """

        url = f"https://www.codechef.com/status/{problem_code}?usernames={user}"

        page_source = self._get_page_source(url)

        soup = BeautifulSoup(page_source, "html.parser")

        rows = soup.find("tbody").find_all("tr")

        for row in rows:
            submission_time = row.find_all("td")[1].span['title']
            submission_time = self._get_time(submission_time)

            is_accepted = row.find_all("td")[3].div.div['title'] == "accepted"

            if is_accepted and  \
               contest_start_time <= submission_time <= contest_start_time + duration:
                return True

        return False

    def _get_page_source(self, url):
        self.driver.get(url)
        return self.driver.page_source

    def _get_time(self, time):
        """
        Convert time obtained from codechef to unix timestamp
        """
        time = time.split('(')[0].strip()
        aware_time = datetime.datetime.strptime(time, "%a %b %d %Y %H:%M:%S %Z%z")

        return aware_time.timestamp()
