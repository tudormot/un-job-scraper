from usecases.usecases import scrape_all_website_usecase
from config.logging_config import config_log

if __name__ == '__main__':
    config_log()
    scrape_all_website_usecase()

