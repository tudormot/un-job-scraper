import logging

from src.scrape.browser_automation.selenium.selenium_automation import \
    SeleniumAutomation
from src.scrape.un_jobs_scraper import UNJobsScraper


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


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def scrape_all_website_usecase():
    scraper = UNJobsScraper(SeleniumAutomation())
    try:
        for job in scraper.get_all_jobs_from_un_jobs():
            print("yay seems like we scraped a job")
            print(job)
    finally:
        scraper.terminate()



def scrape_since_last_update_usecase():
    raise ("Usecase not refactored yet. Refactor first")
    model = icf_model()
    date = model.get_last_update()
    url_list, last_update = get_jobs_since_date(date)
    logging.info('INFO : UNJobs was last updated on: ' + str(last_update))
    logging.info(
        'INFO : icf was last updated on: ' + str(model.get_last_update()))
    logging.info('INFO : uploading ' + str(len(url_list)) + ' jobs')
    upload_from_urls(url_list, model)
    model.set_last_update(last_update)
