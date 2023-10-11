import logging as log
from typing import List

from src.models.job_model import JobModel
from src.storage.tiny_db_dao import TinyDBDAO


class WebsiteToDBSynchronizer:
    def __init__(self, db_dao, icf_adapter):
        self.db: TinyDBDAO = db_dao
        self.icf_adapter = icf_adapter

    def create(self, jobs: List[JobModel]):
        results = self.icf_adapter.upload_jobs(jobs)
        for i, result in enumerate(results):
            if 'success' in result:
                self.db.insert_jobs([jobs[i]])
        return results

    def update_or_create(self, jobs: List[JobModel]):
        self.delete(jobs)
        return self.create(jobs)

    def delete(self, jobs: List[JobModel]):
        log.info('INFO.Deleting jobs.')
        results = self.icf_adapter.delete_jobs(jobs)
        for i, result in enumerate(results):
            if 'success' in result or ('type' in result and result['type']
                                       == "not_exists"):
                self.db.delete_jobs([jobs[i]])

    def terminate(self):
        self.db.terminate()
