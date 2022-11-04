from src.storage.tiny_db_dao import TinyDBDAO
from src.usecases.delete_all_jobs_from_website_usecase import delete_all_jobs
from src.usecases.usecases import scrape_all_website_usecase, \
    scrape_since_last_update_usecase
from src.config.logging_config import config_log


config_log()
db_dao = TinyDBDAO('db.json')
# scrape_since_last_update_usecase()