from datetime import datetime

from typing import Generator, Tuple
import logging as log

from selenium.common.exceptions import WebDriverException, \
    StaleElementReferenceException

from src.models.job_model import JobModel
from src.repository.browser_automation.automation_interface import \
    AutomationInterface
from src.repository.html_parsing.scrape_job_page import JobPageScraper
from src.repository.html_parsing.scrape_main_page import MainPageScraper, JobURLModel

from src.repository.browser_automation.selenium.common import fuzzy_delay

import tracemalloc

tracemalloc.start()


class UNJobsScraper:
    UN_JOBS_MAIN_PAGE_URL = 'https://unjobs.org/new/'

    def __init__(self, web_automation: AutomationInterface):
        self.web_automation = web_automation
        self.main_page_scraper = MainPageScraper(
            UNJobsScraper.UN_JOBS_MAIN_PAGE_URL,
            self.web_automation
        )
        self.job_page_scraper = JobPageScraper(self.web_automation)

    def get_last_un_jobs_update_date(self) -> datetime:
        return self.main_page_scraper.get_last_update_time()

    def get_all_jobs_from_un_jobs(self) -> Generator[
        Tuple[JobModel, JobURLModel], None, None]:
        for job_url_model in self.main_page_scraper.get_all_job_urls():
            try:
                yield (self.job_page_scraper.scrape_job_from_job_page(
                    job_url_model.URL), job_url_model)
            except (WebDriverException, StaleElementReferenceException) \
                    as e:
                print("We caught this error, ", e)
                print("Not sure how to handle, waiting a bit, "
                      "then continuing with next job")
                fuzzy_delay(1)
            except Exception as e:
                log.warning(
                    "could not parse job at url: " + job_url_model.URL)
                log.info("no biggie, continuing with next job")

    def get_jobs_from_un_jobs_since_date(self, date: datetime) -> Generator[
        Tuple[JobModel, JobURLModel], None, None]:
        if self.main_page_scraper.get_last_update_time() > date:
            for job_url_model in \
                    self.main_page_scraper.get_job_urls_since_date(date):
                try:
                    yield (self.job_page_scraper.scrape_job_from_job_page(
                        job_url_model.URL), job_url_model)

                except (WebDriverException, StaleElementReferenceException) \
                        as e:
                    print("We caught this error, ", e)
                    print("Not sure how to handle, waiting a bit, "
                          "then continuing with next job")
                    fuzzy_delay(1)
                except Exception as e:
                    log.warning(
                        "could not parse job at url: " + job_url_model.URL)
                    log.info("no biggie, continuing with next job")

    def terminate(self):
        self.web_automation.terminate()
