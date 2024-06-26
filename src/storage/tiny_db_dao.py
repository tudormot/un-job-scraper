from functools import partial
from typing import List

from tinydb import TinyDB, Query, where
import os
import logging as log
from datetime import datetime, date
import jsonpickle
from pathlib import Path
from src.config.config import args
from src.models.job_model import JobModel


class TinyDBDAO:
    def __init__(self, db_name, enable_asserts=False):
        if args.db_dir is not None:
            dir_path = args.db_dir
        else:
            dir_path = os.path.dirname(os.path.realpath(__file__))
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        db_path = os.path.join(dir_path, db_name)
        self.db_path = db_path
        self.db = TinyDB(self.db_path)
        self.query = Query()
        self.init_database()
        self.delete_all_expired_jobs()

        # this flag enables some db assertions which are useful for
        # debugging, but might slow dows the program
        self.enable_asserts = enable_asserts

    def init_database(self):
        # if db does not contain a last parse date (can happen if db was just
        # created), then populate it here
        if len(self.db.search(self.query.last_updated.exists())) == 0:
            log.warning('Detected that DB does not contain last parsing '
                        'date. This means that DB was just creating. '
                        'populating with very old last_parsing_date')
            self.db.insert({'last_updated':
                                jsonpickle.encode(datetime(1, 1, 1))})  # 1AD

    def delete_all_expired_jobs(self):
        log.info("INFO: deleting expired jobs from TinyDB:")
        curr = datetime.now()
        response = self.db.search(self.query.closing_date.test(partial(
            self._check_job_expired, current_date=curr)))
        log.info("INFO: deleting " + str(len(response)) + " expired jobs.")
        self.db.remove(self.query.closing_date.test(partial(
            self._check_job_expired, current_date=curr)))

    @staticmethod
    def _check_job_expired(date_string: str, current_date: date) -> bool:
        return datetime.strptime(date_string, "%d.%m.%Y") < current_date

    def set_last_update(self, update):
        self.db.remove(self.query.last_updated.exists())
        self.db.insert({'last_updated': jsonpickle.encode(update)})

    def get_last_update(self):
        response = self.db.search(self.query.last_updated.exists())
        assert len(response) == 1, "got more than one last_updated date in db"
        last_update = jsonpickle.decode(response[0]['last_updated'])
        log.info("The last job present in db was updated on unjobs.org at: "
                 ""+ str(last_update))
        return last_update

    def insert_jobs(self, jobs: List[JobModel]):
        for job in jobs:
            if self.enable_asserts:
                assert len(self.db.search(where('id') == job.id)) == 0, \
                    "this job already exists, why are we reinserting it in " \
                    "the db?"
            self.db.insert({
                "id":job.id,
                "closing_date":job.closing_date_to_icf_str_closing_date(
                    job.closing_date),
                "title":job.title
            })

    def delete_jobs(self, jobs: List[JobModel]):
        for job in jobs:
            if self.enable_asserts:
                in_db_count = len(self.db.search(where('id') == job.id))
                assert in_db_count != 1, \
                    "wanted to delete a job, but found it " + str(
                        in_db_count) + "times in the database"
            self.db.remove(where('id') == job.id)

    def terminate(self):
        self.db.close()

    def _delete_underlying_database(self):
        """should not be used for normal operation, but useful for clean
        testing"""
        log.warning("Deleting db from filesystem!")
        os.remove(self.db_path)
