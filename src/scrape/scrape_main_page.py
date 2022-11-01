from dataclasses import dataclass
from typing import List, Generator, Iterable

from src.scrape.browser_automation.automation_interface import \
    AutomationInterface
from bs4 import BeautifulSoup
import logging as log
from datetime import datetime


@dataclass
class JobURLModel:
    URL: str
    upload_date: datetime


class MainPageScraper:
    def __init__(self, page_url, browser_automator):
        self.main_page_url = page_url
        self.browser_automator: AutomationInterface = browser_automator

    def get_job_urls_since_date(self, date: datetime) -> Generator[JobURLModel,
                                                               None, None]:
        # first get to UNJobs page which contains first job already scraped
        print("get_job_urls_since_date was called")
        page_nr = 1
        while True:
            job_list = \
                self._get_urls_from_page(
                    self.main_page_url + str(page_nr))
            log.debug("debug. Latest job from db date: " + str(date))
            log.debug("debug. Oldest job from this page : " + str(job_list[
                -1].upload_date))
            if job_list[-1].upload_date < date:
                log.info("Date on page is older than our date. Starting "
                      "to scrape from page nr: " + str(page_nr))
                first_non_scraped_page = page_nr
                break
            elif page_nr == 40:
                log.warning("Reached end of unjobs website, seems like you "
                            "didn't run the scraper in a long time!")
                first_non_scraped_page = page_nr
                break
            else:
                log.debug("debug. page nr: "+ page_nr + " seems to have a "
                                                        "more "
                                                   "recent date than what is in our database")
                page_nr += 1

        for page_nr in range(first_non_scraped_page, 0, -1):
            job_urls = filter(
                lambda j: j.upload_date > date,
                reversed(
                    self._get_urls_from_page(self.main_page_url + str(
                        page_nr))
                )
            )
            for job in job_urls:
                yield job

    def get_all_job_urls(self) -> Generator[JobURLModel, None, None]:
        for page_nr in range(40, 0, -1):
            jobs_list = self._get_urls_from_page(self.main_page_url + str(
                page_nr))
            if not jobs_list:
                raise Exception("Last time I checked UNJobs.org, they always "
                                "had jobs between pages 40 and 1. This "
                                "exception means that they modified their "
                                "website")
            for job in reversed(jobs_list):
                yield job

    def _get_urls_from_page(self, page_url) -> List[JobURLModel]:
        """ note: the list returned by this function is ordered: IE,
        last element of list is last on UNjobs page, this also meaning that
        it is the one uploaded earliest on the UNjobs website"""
        html = self.browser_automator.get_html_from_url(page_url)
        log.info("INFO. request to : " + str(page_url))
        soup = BeautifulSoup(html, 'html.parser')
        job_url_list = [x['href'] for x in soup.find_all("a", class_="jtitle")]
        date_list = [MainPageScraper._string_to_datetime(x['datetime']) for
                     x in
                     soup.find_all('time', class_='upd timeago')]

        return [
            JobURLModel(
                URL=job_url_list[i],
                upload_date=date_list[i]
            )
            for i in range(len(job_url_list))
        ]

    def get_last_update_time(self) -> datetime:
        html = self.browser_automator.get_html_from_url(self.main_page_url)
        soup = BeautifulSoup(html, 'html.parser')
        tag = soup.find('time', class_='upd timeago')
        last_update_date = MainPageScraper._string_to_datetime(tag['datetime'])
        log.info("INFO: last_update_date: " + str(last_update_date))
        return last_update_date

    @staticmethod
    def _string_to_datetime(s: str) -> datetime:
        return datetime(year=int(s[0:4]), month=int(s[5:7]),
                        day=int(s[8:10]), hour=int(s[11:13]),
                        minute=int(s[14:16]), second=int(s[17:19]))
