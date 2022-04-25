import logging as log
from collections.abc import Generator
from datetime import datetime
from typing import List

from src.rest_adapter import RESTAdapter
from src.rest_adapter_mock import RESTAdapterMock
from src.scrape.browser_automation.selenium.selenium_automation import \
    SeleniumAutomation
from src.scrape.un_jobs_scraper import UNJobsScraper
from src.storage.tiny_db_dao import TinyDBDAO
from src.website_db_sync import WebsiteToDBSynchronizer
from functools import partial


def upload_from_urls(url_list, model):
    raise Exception("needs refactoring and updating")
    CHUNK = 5  # upload only 5 jobs at once
    gen = chunks(url_list, CHUNK)
    while True:
        try:
            urls = next(gen)
            jobs = []
            for url in urls:
                try:
                    job = read_job_from_url(url).as_dict()
                    jobs.append(job)
                    print("DEBUG. Job title: " + job['title'])
                except Exception as e:
                    logging.error("Not able to parse following url : ", url)
                    logging.error("Here is the exception : ", str(e))

            model.update_or_create(jobs)

        except StopIteration as e:
            break


def chunk_generator(initial_gen:Generator, n)->Generator[List,None,None]:
    """Yield successive n-sized chunks from initial generator"""
    chunk = []
    for i in initial_gen:
        chunk.append(i)
        if len(chunk) == n:
            yield chunk.copy()
            chunk = []
    if len(chunk) != 0:
        yield chunk


def scrape_all_website_usecase():
    scraper = UNJobsScraper(SeleniumAutomation())
    scrape_from_job_generator(scraper, scraper.get_all_jobs_from_un_jobs)


def scrape_since_last_update_usecase():
    scraper = UNJobsScraper(SeleniumAutomation())
    temp_db = TinyDBDAO('db.json')
    date = temp_db.get_last_update()
    temp_db.terminate()
    scrape_from_job_generator(scraper,
                              partial(
                                  scraper.get_jobs_from_un_jobs_since_date,
                                  date
                              )
                              )


def scrape_from_job_generator(scraper, job_generator):
    """this function is meant to avoid code duplication. The only thing
    different in our two usecased (scrape since date and since beginning of
    time) is the job generator fun called from the scraper"""
    db_icf_syncer = WebsiteToDBSynchronizer(TinyDBDAO('db.json'),
                                            RESTAdapterMock())
                                            # RESTAdapter())

    unjobs_initial_update_date = scraper.main_page_scraper.get_last_update_time()
    last_successful_parse_upload_date = datetime(1, 1, 1)
    try:
        for job, url_model in job_generator():
            print("yay seems like we scraped a job")
            assert "unjobs.ord" not in job.original_job_link, "bad job link " \
                                                              "problem still here for job " + job.original_job_link
            db_icf_syncer.update_or_create([job])
            last_successful_parse_upload_date = url_model.upload_date
    finally:
        log.info("Setting last update in DB from unjobs upload date of last "
                 "successfully scraped job: " +
                 str(last_successful_parse_upload_date))
        db_icf_syncer.db.set_last_update(last_successful_parse_upload_date)
        unjobs_final_update_date = \
            scraper.main_page_scraper.get_last_update_time()
        if unjobs_final_update_date != unjobs_initial_update_date:
            log.warning("the update time reported by unjobs.com was modified "
                        "from the begining of the parsing to the end of it. "
                        "This means that unjobs.com has been updated with "
                        "mode jobs during our scraping. This should not be a "
                        "big problem, it should just mean that we missed "
                        "scraping a few jobs..but no biggie")

        scraper.terminate()
        db_icf_syncer.terminate()
