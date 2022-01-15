from dataclasses import dataclass
from typing import List

from src.scrape.common import get_html_from_url
from src.utils import fuzzy_delay
from bs4 import BeautifulSoup
import logging as log
from datetime import datetime


@dataclass
class JobURLModel:
    URL:str
    upload_date:datetime

class MainPageScraper:
    def __init__(self, page_url, web_driver):
        self.page_url = page_url
        self.web_driver = web_driver

    def get_jobs_since_date(self, date):
        url_list = []
        page_nr = 1
        break_loop = False
        while True:
            job_list:List[JobURLModel] = \
                self._get_urls_from_page(
                    self.page_url + str(page_nr))
            for job in job_list:
                if job.upload_date > date:
                    url_list.append(job.URL)
                else:
                    break_loop = True
                    break
            if break_loop:
                break

            if not job_list:
                log.critical('Did not find any more pages at url: ' + str(
                    self.page_url + str(page_nr)))
                break
            page_nr += 1

        return url_list

    def get_all_job_urls(self):
        page_nr = 1

        while True:
            jobs_list = self._get_urls_from_page(self.page_url + str(
                page_nr))
            if not jobs_list:
                log.info(
                    'Did not find any more pages at url: ' + str(
                        self.page_url) +
                    str(
                        page_nr))
                break
            for job in jobs_list:
                yield job.URL
            page_nr += 1

    def _get_urls_from_page(self, page_url)->List[JobURLModel]:
        html = get_html_from_url(page_url, self.web_driver)
        fuzzy_delay(1)
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
        html, _ = get_html_from_url(self.page_url, self.web_driver)
        fuzzy_delay(1)
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
