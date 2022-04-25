from src.models.job_model import JobModel
from src.rest_adapter import RESTAdapter
from src.scrape.browser_automation.selenium.common import fuzzy_delay
from src.storage.tiny_db_dao import TinyDBDAO
from src.website_db_sync import WebsiteToDBSynchronizer


def delete_all_jobs():
    db_dao = TinyDBDAO('db.json')
    db_icf_syncer = WebsiteToDBSynchronizer(db_dao,
                                            RESTAdapter())
    for item in db_dao.db:
        if 'id' in item:
            dummy_job = JobModel()
            dummy_job.id = item['id']
            db_icf_syncer.delete([dummy_job])
            fuzzy_delay(0.1)
