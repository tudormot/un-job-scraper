from src.control.delete_all_jobs_from_website_usecase import delete_all_jobs
from src.control.usecases import scrape_all_website_usecase, \
    scrape_since_last_update_usecase
from src.config.logging_config import config_log


config_log()
scrape_since_last_update_usecase()