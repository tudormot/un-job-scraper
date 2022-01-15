from datetime import datetime

from typing import Generator

from src.models.job_model import JobModel
from src.scrape.scrape_job_page import JobPageScraper
from src.scrape.scrape_main_page import MainPageScraper
from src.scrape.web_driver import web_driver


class UNJobsScraper:
    UN_JOBS_MAIN_PAGE_URL = 'https://unjobs.org/new/'

    def __init__(self):
        self.web_driver = web_driver
        self.main_page_scraper = MainPageScraper(
            UNJobsScraper.UN_JOBS_MAIN_PAGE_URL,
            self.web_driver
        )
        self.job_page_scraper = JobPageScraper(self.web_driver)

    def get_last_un_jobs_update_date(self) -> datetime:
        return self.main_page_scraper.get_last_update_time()

    def get_all_jobs_from_un_jobs(self) -> Generator[JobModel, None, None]:
        for job_url in self.main_page_scraper.get_all_job_urls():
            yield self.job_page_scraper.scrape_job_from_job_page(job_url)

    def get_jobs_from_un_jobs_since_date(self, date: datetime) -> Generator[
        JobModel, None, None]:
        raise Exception("WIP Not reimplemented yet!2")
        pass
