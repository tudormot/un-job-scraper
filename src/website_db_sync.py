import logging as log

from src.rest_adapter import RESTAdapter
from src.storage.tiny_db_dao import TinyDBDAO


class WebsiteToDBSynchronizer:
    def __init__(self):
        self.db = TinyDBDAO()
        self.icf_adapter = RESTAdapter()

    def create(self, jobs):
        results = self.icf_adapter.upload_jobs(jobs)
        for i, result in enumerate(results):
            if 'success' in result:
                self.db.insert_job(jobs[i])
        return results

    def update_or_create(self, jobs):
        self.delete(jobs)
        self.create(jobs)

    def delete(self, jobs):
        log.info('INFO.Deleting jobs.')
        results = self.icf_adapter.delete_jobs(jobs)
        for i, result in enumerate(results):
            if 'success' in result or ('type' in result and result['type']
                                       == "not_exists"):
                self.db.delete_jobs(self.query.id == jobs[i]["id"])
