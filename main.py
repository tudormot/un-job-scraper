

from scrape_main_page import *
from scraping import *
from icf_model import *






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
                except Exception as e:
                    print("Not able to parse following url : ", url)
                    print("Here is the exception : ", str(e))

            model.create(jobs)

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

def scrape_since_last_update_usecase():
    model = icf_model()
    date = model.get_last_update()
    url_list, last_update = get_jobs_since_date(date)
    print(url_list)
    print('UNJobs was last updated on: ', str(last_update))
    print('icf was last updated on: ', str(model.get_last_update()))
    # upload_from_urls(url_list, model)
    # model.set_last_update(last_update)






if __name__ == '__main__':
    # jobs = read_html_from_file()
    # save_jobs_as_JSON(jobs)
    # import codecs
    # data = json.load(codecs.open('example_v3.json', 'r', 'utf-8-sig'))
    # upload_jobs(data)
    # scrape_all_website_usecase()
    scrape_since_last_update_usecase()
    pass

