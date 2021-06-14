from scrape_main_page import *
from scraping import *
from icf_model import icf_model
import logging






def upload_from_urls(url_list,model):
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
    model = icf_model()
    url_list, last_update = get_all_job_urls()
    upload_from_urls(url_list,model)
    model.set_last_update(last_update)

def delete_expired_jobs_usecase():
    model = icf_model()
    model.delete_expired_jobs()

def scrape_since_last_update_usecase():
    model = icf_model()
    date = model.get_last_update()
    url_list, last_update = get_jobs_since_date(date)
    logging.info('INFO : UNJobs was last updated on: '+ str(last_update))
    logging.info('INFO : icf was last updated on: '+ str(model.get_last_update()))
    logging.info('INFO : uploading '+str(len(url_list))+' jobs')
    upload_from_urls(url_list, model)
    model.set_last_update(last_update)

