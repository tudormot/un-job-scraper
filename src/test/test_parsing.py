import datetime
import logging
import random
import time
import unittest

from src.models.job_model import JobModel
from src.scrape.browser_automation.selenium.selenium_automation import \
    SeleniumAutomation
from src.scrape.scrape_main_page import JobURLModel
from src.scrape.un_jobs_scraper import UNJobsScraper
import logging as log


class MainPageScraperTesting(unittest.TestCase):
    def setUp(self) -> None:
        # logging.getLogger().setLevel(logging.DEBUG)
        self.un_parser = UNJobsScraper(SeleniumAutomation())
        self.addCleanup(self.un_parser.terminate)

    def test_0_number_of_jobs_per_page(self):
        test_url = "https://unjobs.org/new/1"
        job_url_list = self.un_parser.main_page_scraper._get_urls_from_page(
            test_url)
        self.assertEqual(len(job_url_list), 25, "Since when are there no 25 "
                                                "jobs per page?")

    def test_1_jobs_in_increasing_date_order(self):
        job_url_list: list[JobURLModel] = \
            self.un_parser.main_page_scraper._get_urls_from_page(
                UNJobsScraper.UN_JOBS_MAIN_PAGE_URL + '1')
        for i, job in enumerate(job_url_list[:-1]):
            self.assertTrue(job.upload_date > job_url_list[i + 1].upload_date,
                            "job upload dates not ordered as we expected")

    def test_2_parse_first_job(self):
        job_url_list = self.un_parser.main_page_scraper._get_urls_from_page(
            UNJobsScraper.UN_JOBS_MAIN_PAGE_URL + '1')
        job: JobModel = \
            self.un_parser.job_page_scraper.scrape_job_from_job_page(
                job_url_list[0].URL)
        self.assertTrue(job.title != "" and job.title, "title not parsed?!")
        self.assertTrue(job.id != "" and job.id, "id not parsed?!")
        self.assertTrue(job.organisation != "" and job.organisation,
                        "organisation not parsed?!")
        self.assertTrue(job.country != "" and job.country,
                        "country not parsed?!")
        self.assertTrue(job.city != "" and job.city, "city not parsed?!")
        self.assertTrue(job.closing_date != "" and job.closing_date,
                        "closing_date not parsed?!")
        self.assertTrue(len(job.tags) != 0 and job.tags, "tags not parsed?!")
        self.assertTrue(job.job_type is not None, "job_type not parsed?!")

    def test_3_get_job_urls_after_date(self):
        # first get the date of a job from the 2nd page:
        jobs_temp = self.un_parser.main_page_scraper._get_urls_from_page(
            UNJobsScraper.UN_JOBS_MAIN_PAGE_URL + '2'
        )
        fake_last_update_date = random.choice(jobs_temp).upload_date
        jobs = self.un_parser.main_page_scraper.get_job_urls_since_date(
            fake_last_update_date)
        count = 0
        for job in jobs:
            self.assertTrue(job.upload_date > fake_last_update_date,
                            "parsed jobs older than fake last update date! "
                            "job: " + str(job))
            count += 1
        self.assertTrue(25 < count <= 50,
                        "since we got the fake date from a job from the 2nd "
                        "page, we were expecting between 25 and 50 jobs. We "
                        "got: " + str(count))

    def test_4_get_last_update_time(self):
        last_update_time = self.un_parser.main_page_scraper.\
            get_last_update_time()
        delta = datetime.datetime.today() - last_update_time
        log.info("last_update_time: " + str(last_update_time))
        self.assertTrue(delta.days < 4, "last_update_time bigger than 4 "
                                        "days. Weird, check again unjobs "
                                        "website. last_update_time: "
                        + str(last_update_time))


if __name__ == '__main__':
    unittest.main()
