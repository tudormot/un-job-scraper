from usecases import *
from logging_config import config_log





if __name__ == '__main__':
    # jobs = read_html_from_file()
    # save_jobs_as_JSON(jobs)
    # import codecs
    # data = json.load(codecs.open('example_v5.json', 'r', 'utf-8-sig'))
    # upload_jobs(data)
    # scrape_all_website_usecase()
    config_log()
    scrape_since_last_update_usecase()
    # delete_expired_jobs_usecase()
    pass

