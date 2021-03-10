from web_adapter import *
from tinydb import TinyDB, Query
import datetime
import logging as l
import os
dir_path = os.path.dirname(os.path.realpath(__file__))



class icf_model:
    def __init__(self):
        self.db = TinyDB(os.path.join(dir_path,'db.json'))
        self.query = Query()
        self.delete_expired_jobs()

    def delete_expired_jobs(self):
        l.info("INFO: deleting expired jobs")
        curr = datetime.datetime.now()
        test_func = lambda s: self._closingdatestr_to_date(s) < curr
        response = self.db.search(self.query.closing_date.test(test_func))
        l.info("INFO: deleting "+str(len(response))+" expired jobs.")
        self.delete(response)
        # self.db.remove(self.query.closing_date.test(test_func))


    def create(self, jobs):
        results = request_with_retry(jobs,upload_jobs)
        for i, result in enumerate(results):
            if 'success' in result:
                self.db.insert(jobs[i])
        return results

    def update_or_create(self,jobs):
        # just a deletion of jobs followed by creation
        # first check if the jobs exist by job id
        all_ids = [job['id'] for job in jobs]
        found = self.db.search(self.query.id.test(lambda id: id in all_ids))
        #delete the entries already found from website and DB
        if found: #aka if found is non-empty, stupid python syntax
            self.delete(found)

        #now create all jobs.. Everything should be successful as the pre-existing ones should have been deleted
        self.create(jobs)


    def delete(self,jobs):
        l.info('INFO.Deleting jobs.')
        results = request_with_retry(jobs,delete_jobs)
        #also delete jobs from db
        for i, result in enumerate(results):
            if 'success' in result or 'type' in result and result['type']=="not_exists":
                self.db.remove(self.query.id == jobs[i]["id"])



    def set_last_update(self,update):
        self.db.remove(self.query.last_updated.exists())
        self.db.insert({'last_updated':str(update)})

    def get_last_update(self):
        response = self.db.search(self.query.last_updated.exists())
        return self._str_to_date(response[0]['last_updated'])

    @staticmethod
    def _str_to_date(s):
        "eg date : 2021-01-15 09:20:06"
        return datetime.datetime(year = int(s[0:4]),
                                 month=int(s[5:7]),
                                 day=int(s[8:10]),
                                 hour=int(s[11:13]),
                                 minute=int(s[14:16]),
                                 second=int(s[17:19]))

    @staticmethod
    def _closingdatestr_to_date(s):
        list = s.split('.')
        return datetime.datetime(year = int(list[2]),
                                 month= int(list[1]),
                                 day=int(list[0]),
                                 hour=int(23),
                                 minute=int(59),
                                 second=int(59))