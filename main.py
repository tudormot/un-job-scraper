

from scrape_main_page import *
from scraping import *
from icf_model import *










def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def scrape_all_website_usecase():
    model = icf_model()
    CHUNK = 5 #upload only 5 jobs at once
    url_list, last_update = get_all_job_urls()
    # url_list = ['https://unjobs.org/vacancies/1610310129145', 'https://unjobs.org/vacancies/1610310134555']
    # last_update = datetime.datetime.now()
    gen = chunks(url_list,CHUNK)
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
    model.set_last_update(last_update)




if __name__ == '__main__':
    # jobs = read_html_from_file()
    # save_jobs_as_JSON(jobs)
    # import codecs
    # data = json.load(codecs.open('example_v2.json', 'r', 'utf-8-sig'))
    # upload_jobs(data)
    scrape_all_website_usecase()
    # scrape_all_website_usecase()

