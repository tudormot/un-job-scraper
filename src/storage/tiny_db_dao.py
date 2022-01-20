from tinydb import TinyDB, Query
import os
import logging as log
from datetime import datetime


class TinyDBDAO:
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.db = TinyDB(os.path.join(dir_path, 'db.json'))
        self.query = Query()
        self.init_database()
        self.delete_all_expired_jobs()

    def init_database(self):
        # if db does not contain a last parse date (can happen if db was just
        # created), then populate it here
        if self.db.search(self.query.last_updated.exists()) is None:
            log.warning('Detected that DB does not contain last parsing '
                        'date. This means that DB was just creating. '
                        'populating with very old last_parsing_date')
            self.db.insert({'last_updated': datetime(1, 1, 1)})  # year 1AD

    def delete_all_expired_jobs(self):
        log.info("INFO: deleting expired jobs from TinyDB:")
        curr = datetime.datetime.now()
        test_func = lambda s: self._closingdatestr_to_date(s) < curr
        response = self.db.search(self.query.closing_date.test(test_func))
        log.info("INFO: deleting " + str(len(response)) + " expired jobs.")
        self.db.remove(self.query.closing_date.test(test_func))

    def set_last_update(self, update):
        self.db.remove(self.query.last_updated.exists())
        self.db.insert({'last_updated': str(update)})

    def get_last_update(self):
        response = self.db.search(self.query.last_updated.exists())
        return self._str_to_date(response[0]['last_updated'])

    def insert_job(self, job):
        self.db.insert(job)

    def delete_jobs(self, job):
        self.db.remove(job)

    @staticmethod
    def _str_to_date(s):
        "eg date : 2021-01-15 09:20:06"
        return datetime.datetime(year=int(s[0:4]),
                                 month=int(s[5:7]),
                                 day=int(s[8:10]),
                                 hour=int(s[11:13]),
                                 minute=int(s[14:16]),
                                 second=int(s[17:19]))

    @staticmethod
    def _closingdatestr_to_date(s):
        list = s.split('.')
        return datetime.datetime(year=int(list[2]),
                                 month=int(list[1]),
                                 day=int(list[0]),
                                 hour=int(23),
                                 minute=int(59),
                                 second=int(59))
